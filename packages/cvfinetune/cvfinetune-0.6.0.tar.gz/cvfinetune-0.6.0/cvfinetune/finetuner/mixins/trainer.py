import abc
import logging
import pyaml

from bdb import BdbQuit
from chainer.serializers import save_npz
from chainer.training import extensions
from cvdatasets.utils import pretty_print_dict
from pathlib import Path


class _TrainerMixin(abc.ABC):
	"""This mixin is responsible for updater, evaluator and trainer creation.
	Furthermore, it implements the run method
	"""

	def __init__(self, opts, updater_cls, updater_kwargs={}, *args, **kwargs):
		super(_TrainerMixin, self).__init__(*args, **kwargs)
		self.updater_cls = updater_cls
		self.updater_kwargs = updater_kwargs

	def init_updater(self):
		"""Creates an updater from training iterator and the optimizer."""

		if self.opt is None:
			self.updater = None
			return

		self.updater = self.updater_cls(
			iterator=self.train_iter,
			optimizer=self.opt,
			device=self.device,
			**self.updater_kwargs,
		)
		logging.info(" ".join([
			f"Using single GPU: {self.device}.",
			f"{self.updater_cls.__name__} is initialized",
			f"with following kwargs: {pretty_print_dict(self.updater_kwargs)}"
			])
		)

	def init_evaluator(self, default_name="val"):
		"""Creates evaluation extension from validation iterator and the classifier."""

		self.evaluator = extensions.Evaluator(
			iterator=self.val_iter,
			target=self.clf,
			device=self.device,
			progress_bar=True
		)

		self.evaluator.default_name = default_name

	def _new_trainer(self, trainer_cls, opts, *args, **kwargs):
		return trainer_cls(
			opts=opts,
			updater=self.updater,
			evaluator=self.evaluator,
			*args, **kwargs
		)

	def run(self, trainer_cls, opts, *args, **kwargs):

		trainer = self._new_trainer(trainer_cls, opts, *args, **kwargs)

		self.save_meta_info(opts, folder=Path(trainer.out, "meta"))

		logging.info("Snapshotting is {}abled".format("dis" if opts.no_snapshot else "en"))

		def dump(suffix):
			if opts.only_eval or opts.no_snapshot:
				return

			save_npz(Path(trainer.out, f"clf_{suffix}.npz"), self.clf)
			save_npz(Path(trainer.out, f"model_{suffix}.npz"), self.model)

		try:
			trainer.run(opts.init_eval or opts.only_eval)
		except (KeyboardInterrupt, BdbQuit) as e:
			raise e
		except Exception as e:
			dump("exception")
			raise e
		else:
			dump("final")

	def save_meta_info(self, opts, folder: Path):
		folder.mkdir(parents=True, exist_ok=True)

		with open(folder / "args.yml", "w") as f:
			pyaml.dump(opts.__dict__, f, sort_keys=True)

