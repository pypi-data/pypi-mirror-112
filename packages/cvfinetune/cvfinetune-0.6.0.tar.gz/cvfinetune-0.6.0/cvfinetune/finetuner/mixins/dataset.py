import abc
import logging

from cvdatasets import AnnotationType
from cvdatasets.dataset.image import Size
from cvdatasets.utils import new_iterator


class _DatasetMixin(abc.ABC):
	"""
		This mixin is responsible for annotation loading and for
		dataset and iterator creation.
	"""

	def __init__(self, opts, dataset_cls, dataset_kwargs_factory, *args, **kwargs):
		super(_DatasetMixin, self).__init__(opts=opts, *args, **kwargs)
		self.annot = None
		self.dataset_type = opts.dataset
		self.dataset_cls = dataset_cls
		self.dataset_kwargs_factory = dataset_kwargs_factory

	@property
	def n_classes(self):
		return self.ds_info.n_classes + self.dataset_cls.label_shift

	@property
	def data_info(self):
		assert self.annot is not None, "annot attribute was not set!"
		return self.annot.info

	@property
	def ds_info(self):
		return self.data_info.DATASETS[self.dataset_type]

	def new_dataset(self, opts, size, part_size, subset):
		"""Creates a dataset for a specific subset and certain options"""
		if self.dataset_kwargs_factory is not None and callable(self.dataset_kwargs_factory):
			kwargs = self.dataset_kwargs_factory(opts, subset)
		else:
			kwargs = dict()

		kwargs = dict(kwargs,
			subset=subset,
			dataset_cls=self.dataset_cls,
			prepare=self.prepare,
			size=size,
			part_size=part_size,
			center_crop_on_val=getattr(opts, "center_crop_on_val", False),
		)


		ds = self.annot.new_dataset(**kwargs)
		logging.info("Loaded {} images".format(len(ds)))
		return ds


	def read_annotations(self, opts):
		"""Reads annotations and creates annotation instance, which holds important infos about the dataset"""

		self.annot = AnnotationType.new_annotation(opts, load_strict=False)
		self.dataset_cls.label_shift = opts.label_shift


	def init_datasets(self, opts):

		size = Size(opts.input_size)
		part_size = getattr(opts, "parts_input_size", None)
		part_size = size if part_size is None else Size(part_size)

		logging.info(" ".join([
			f"Image input size: {size}",
			f"Image parts input size: {part_size}",
		]))

		self.train_data = self.new_dataset(opts, size, part_size, "train")
		self.val_data = self.new_dataset(opts, size, part_size, "test")

	def init_iterators(self, opts):
		"""Creates training and validation iterators from training and validation datasets"""

		kwargs = dict(n_jobs=opts.n_jobs, batch_size=opts.batch_size)

		if hasattr(self.train_data, "new_iterator"):
			self.train_iter, _ = self.train_data.new_iterator(**kwargs)
		else:
			self.train_iter, _ = new_iterator(self.train_data, **kwargs)

		if hasattr(self.val_data, "new_iterator"):
			self.val_iter, _ = self.val_data.new_iterator(**kwargs,
				repeat=False, shuffle=False
			)
		else:
			self.val_iter, _ = new_iterator(self.val_data,
				**kwargs, repeat=False, shuffle=False
			)

