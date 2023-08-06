"""
here you can find some model definitions or modificated versions
of present models in chainer (eg. VGG19)
"""

from functools import partial

from chainer_addons.models.base import ModelWrapper
from chainer_addons.models.alexnet import AlexNet
from chainer_addons.models.classifier import Classifier
from chainer_addons.models.classifier import RNNClassifier
from chainer_addons.models.efficientnet import EfficientNetLayers
from chainer_addons.models.inception import InceptionV3
from chainer_addons.models.resnet import Resnet35Layers
from chainer_addons.models.resnet import ResnetLayers
from chainer_addons.models.vgg import VGG19Layers

from chainer_addons.utils import imgproc

from cvargparse.utils.enumerations import BaseChoiceType

class ModelType(BaseChoiceType):
	ResNet = ResnetLayers
	VGG19 = VGG19Layers
	Inception = InceptionV3
	EfficientNet = EfficientNetLayers

	Default = InceptionV3

	def __call__(self, *args, **kwargs):
		"""
			Initializes new model instance
		"""
		model_cls = self.value
		model = model_cls(*args, **kwargs)
		return model

	@classmethod
	def new(cls, model_type, input_size=None, pooling="g_avg", pooling_params={}, aux_logits=False):

		model_type = cls[model_type]
		kwargs = dict(
			pooling=pooling,
			pooling_params=pooling_params
		)

		if model_type == cls.Inception:
			kwargs["aux_logits"] = aux_logits


		model = model_type(**kwargs)

		if input_size is not None:
			model.meta.input_size = input_size

		return model



class PrepareType(BaseChoiceType):
	MODEL = 0
	CUSTOM = 1
	TF = 2
	CHAINERCV2 = 3

	Default = CUSTOM

	def __call__(self, model):
		"""
			Initializes image preprocessing function
		"""

		if self == PrepareType.MODEL:
			return model.meta.prepare_func

		elif self == PrepareType.CUSTOM:
			return imgproc.GenericPrepare(
				size=model.meta.input_size)

		elif self == PrepareType.TF:
			return imgproc.GenericTFPrepare(
				size=model.meta.input_size,
				from_path=False)

		elif self == PrepareType.CHAINERCV2:
			return imgproc.ChainerCV2Prepare(
				size=model.meta.input_size)

