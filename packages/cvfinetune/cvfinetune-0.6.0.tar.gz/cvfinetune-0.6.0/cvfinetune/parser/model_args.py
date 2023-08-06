import abc

from chainer_addons.links import PoolingType
from chainer_addons.models import PrepareType
from cvargparse import Arg
from cvargparse import BaseParser
from cvfinetune.parser.utils import parser_extender
from cvmodelz.models import ModelFactory

@parser_extender
def add_model_args(parser: BaseParser) -> None:

	choices = ModelFactory.get_models(["chainercv2", "cvmodelz"])
	_args = [
		Arg("--model_type", "-mt",
			required=True,
			choices=choices,
			help="type of the model"),

		Arg("--pre_training", "-pt",
			default="imagenet",
			choices=["imagenet", "inat"],
			help="type of model pre-training"),

		Arg("--input_size", type=int, nargs="+", default=0,
			help="overrides default input size of the model, if greater than 0"),

		Arg("--parts_input_size", type=int, nargs="+", default=0,
			help="overrides default input part size of the model, if greater than 0"),

		PrepareType.as_arg("prepare_type",
			help_text="type of image preprocessing"),

		PoolingType.as_arg("pooling",
			help_text="type of pre-classification pooling"),

		Arg("--load", type=str,
			help="ignore weights and load already fine-tuned model (classifier will NOT be re-initialized and number of classes will be unchanged)"),

		Arg("--weights", type=str,
			help="ignore default weights and load already pre-trained model (classifier will be re-initialized and number of classes will be changed)"),

		Arg("--headless", action="store_true",
			help="ignores classifier layer during loading"),

		Arg("--load_strict", action="store_true",
			help="load weights in a strict mode"),

		Arg("--load_path", type=str, default="",
			help="load path within the weights archive"),
	]

	parser.add_args(_args, group_name="Model arguments")


class ModelParserMixin(abc.ABC):
	def __init__(self, *args, **kwargs):
		super(ModelParserMixin, self).__init__(*args, **kwargs)
		add_model_args(self)


__all__ = [
	"ModelParserMixin",
	"add_model_args"
]
