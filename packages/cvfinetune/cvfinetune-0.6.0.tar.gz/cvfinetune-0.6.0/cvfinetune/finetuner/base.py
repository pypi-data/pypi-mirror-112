import chainer

from chainer.backends import cuda

from cvfinetune.finetuner import mixins

class DefaultFinetuner(mixins._ModelMixin, mixins._DatasetMixin, mixins._TrainerMixin):
	""" The default Finetuner gathers together the creations of all needed
	components and call them in the correct order

	"""

	def __init__(self, opts, *args, **kwargs):
		super(DefaultFinetuner, self).__init__(opts=opts, *args, **kwargs)

		self.gpu_config(opts)
		self.read_annotations(opts)

		self.init_model(opts)
		self.init_datasets(opts)
		self.init_iterators(opts)

		self.init_classifier(opts)
		self.load_weights(opts)

		self.init_optimizer(opts)
		self.init_updater()
		self.init_evaluator()

	def init_device(self):
		self.device = cuda.get_device_from_id(self.device_id)
		self.device.use()
		return self.device


	def gpu_config(self, opts):
		if -1 in opts.gpu:
			self.device_id = -1
		else:
			self.device_id = opts.gpu[0]

		return self.init_device()

