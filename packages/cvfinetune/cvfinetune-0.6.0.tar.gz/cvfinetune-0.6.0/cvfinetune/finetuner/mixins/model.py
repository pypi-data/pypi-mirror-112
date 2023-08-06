import abc
import chainer
import logging

from chainer import functions as F
from chainer.optimizer_hooks import Lasso
from chainer.optimizer_hooks import WeightDecay
from chainer_addons.functions import smoothed_cross_entropy
from chainer_addons.models import PrepareType
from chainer_addons.training import optimizer
from chainer_addons.training import optimizer_hooks
from chainercv2.models import model_store
from cvdatasets.dataset.image import Size
from cvdatasets.utils import pretty_print_dict
from cvmodelz.models import ModelFactory
from functools import partial
from pathlib import Path
from typing import Tuple

def check_param_for_decay(param):
	return param.name != "alpha"

def enable_only_head(chain: chainer.Chain):
	if hasattr(chain, "enable_only_head") and callable(chain.enable_only_head):
		chain.enable_only_head()

	else:
		chain.disable_update()
		chain.fc.enable_update()


class _ModelMixin(abc.ABC):
	"""
		This mixin is responsible for optimizer creation, model creation,
		model wrapping around a classifier and model weights loading.
	"""

	def __init__(self, opts, classifier_cls, classifier_kwargs={}, model_kwargs={}, *args, **kwargs):
		super(_ModelMixin, self).__init__(opts=opts, *args, **kwargs)
		self.classifier_cls = classifier_cls
		self.classifier_kwargs = classifier_kwargs
		self.model_type = opts.model_type
		self.model_kwargs = model_kwargs


	@property
	def model_info(self):
		return self.data_info.MODELS[self.model_type]

	def init_model(self, opts):
		"""creates backbone CNN model. This model is wrapped around the classifier later"""

		self.model = ModelFactory.new(self.model_type,
			input_size=Size(opts.input_size),
			**self.model_kwargs
		)


		if self.model_type.startswith("chainercv2"):
			opts.prepare_type = "chainercv2"

		self.prepare = partial(PrepareType[opts.prepare_type](self.model),
			swap_channels=opts.swap_channels,
			keep_ratio=getattr(opts, "center_crop_on_val", False),
		)

		logging.info(
			f"Created {self.model.__class__.__name__} model "
			f" with \"{opts.prepare_type}\" prepare function."
		)


	def init_classifier(self, opts):

		clf_class, kwargs = self.classifier_cls, self.classifier_kwargs

		self.clf = clf_class(
			model=self.model,
			loss_func=self._loss_func(opts),
			**kwargs)

		logging.info(
			f"Wrapped the model around {clf_class.__name__}"
			f" with kwargs: {pretty_print_dict(kwargs)}"
		)

	def _loss_func(self, opts):
		if getattr(opts, "l1_loss", False):
			return F.hinge

		label_smoothing = getattr(opts, "label_smoothing", 0)
		if label_smoothing > 0:
			assert label_smoothing < 1, "Label smoothing factor must be less than 1!"

			return partial(smoothed_cross_entropy, N=self.n_classes, eps=label_smoothing)

		return F.softmax_cross_entropy

	def init_optimizer(self, opts):
		"""Creates an optimizer for the classifier """
		if not hasattr(opts, "optimizer"):
			self.opt = None
			return

		opt_kwargs = {}
		if opts.optimizer == "rmsprop":
			opt_kwargs["alpha"] = 0.9

		if opts.optimizer in ["rmsprop", "adam"]:
			opt_kwargs["eps"] = 1e-6

		self.opt = optimizer(opts.optimizer,
			self.clf,
			opts.learning_rate,
			decay=0, gradient_clipping=False, **opt_kwargs
		)

		logging.info(
			f"Initialized {self.opt.__class__.__name__} optimizer"
			f" with initial LR {opts.learning_rate} and kwargs: {pretty_print_dict(opt_kwargs)}"
		)

		if opts.decay > 0:
			reg_kwargs = {}
			if opts.l1_loss:
				reg_cls = Lasso

			elif opts.pooling == "alpha":
				reg_cls = optimizer_hooks.SelectiveWeightDecay
				reg_kwargs["selection"] = check_param_for_decay

			else:
				reg_cls = WeightDecay

			logging.info(f"Adding {reg_cls.__name__} ({opts.decay:e})")
			self.opt.add_hook(reg_cls(opts.decay, **reg_kwargs))

		if getattr(opts, "only_head", False):
			assert not getattr(opts, "recurrent", False), \
				"Recurrent classifier is not supported with only_head option!"

			logging.warning("========= Fine-tuning only classifier layer! =========")
			enable_only_head(self.clf)


	def _get_loader(self, opts) -> Tuple[bool, str]:
		if getattr(opts, "from_scratch", False):
			logging.info("Training a {0.__class__.__name__} model from scratch!".format(self.model))
			return None, None

		if getattr(opts, "load", None):
			weights = getattr(opts, "load", None)
			logging.info(f"Loading already fine-tuned weights from \"{weights}\"")
			return False, weights

		elif getattr(opts, "weights", None):
			weights = getattr(opts, "weights", None)
			logging.info(f"Loading custom fine-tuned weights from \"{weights}\"")
			return True, weights

		else:
			weights = self._default_weights(opts)
			logging.info(f"Loading custom fine-tuned weights from \"{weights}\"")
			return True, weights

	def _default_weights(self, opts):
		if self.model_type.startswith("chainercv2"):
			model_name = self.model_type.split(".")[-1]
			return model_store.get_model_file(
				model_name=model_name,
				local_model_store_dir_path=str(Path.home() / ".chainer" / "models"))

		else:
			ds_info = self.data_info
			model_info = self.model_info

			base_dir = Path(ds_info.BASE_DIR)
			weights_dir = base_dir / ds_info.MODEL_DIR / model_info.folder

			weights = model_info.weights
			assert opts.pre_training in weights, \
				f"Weights for \"{opts.pre_training}\" pre-training were not found!"

			return str(weights_dir / weights[opts.pre_training])


	def load_weights(self, opts) -> None:

		finetune, weights = self._get_loader(opts)

		self.clf.load(weights,
			n_classes=self.n_classes,
			finetune=finetune,

			path=opts.load_path,
			strict=opts.load_strict,
			headless=opts.headless
		)

		self.clf.cleargrads()

		feat_size = self.model.meta.feature_size

		if hasattr(self.clf, "output_size"):
			feat_size = self.clf.output_size

		### TODO: handle feature size!

		logging.info(f"Part features size after encoding: {feat_size}")
