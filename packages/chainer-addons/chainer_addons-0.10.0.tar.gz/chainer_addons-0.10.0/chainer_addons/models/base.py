import abc
import chainer
import chainer.functions as F
import numpy as np

from chainer.initializers import HeNormal
from chainer.serializers import npz
from collections import OrderedDict
from functools import reduce

from chainer_addons.links import PoolingType


class BaseModel(abc.ABC):
	class meta(object):
		input_size = None
		feature_size = None
		classifier_layers = [None]
		conv_map_layer = None
		feature_layer = None

		@classmethod
		def prepare_func(cls, *args, **kwargs):
			raise NotImplementedError()

	@abc.abstractproperty
	def model_instance(self):
		raise NotImplementedError()

	@property
	def clf_layer_name(self):
		return self.meta.classifier_layers[-1]

	@property
	def clf_layer(self):
		return reduce(lambda obj, attr: getattr(obj, attr),
			self.clf_layer_name.split("/"), self.model_instance)
		# return getattr(self.model_instance, self.clf_layer_name)

	def loss(self, pred, gt, loss_func=F.softmax_cross_entropy):
		return loss_func(pred, gt)

	def accuracy(self, pred, gt):
		return F.accuracy(pred, gt)


	def load_for_finetune(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			The weights should be pre-trained on a bigger
			dataset (eg. ImageNet). The classification layer is
			reinitialized after all other weights are loaded
		"""
		self.load(weights, path=path, strict=strict, headless=headless)
		self.reinitialize_clf(n_classes, **kwargs)

	def load_for_inference(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			In this use case we are loading already fine-tuned
			weights. This means, we need to reinitialize the
			classification layer first and then load the weights.
		"""
		self.reinitialize_clf(n_classes, **kwargs)
		self.load(weights, path=path, strict=strict, headless=headless)

	def load(self, weights, *, path="", strict=False, headless=False):
		if weights not in [None, "auto"]:
			ignore_names = None
			if headless:
				ignore_names = lambda name: name.startswith(path + self.clf_layer_name)

			npz.load_npz(weights, self.model_instance,
				path=path, strict=strict, ignore_names=ignore_names)

	def reinitialize_clf(self, n_classes,
		feat_size=None, initializer=None):
		if initializer is None or not callable(initializer):
			initializer = HeNormal(scale=1.0)

		clf_layer = self.clf_layer

		w_shape = (n_classes, feat_size or clf_layer.W.shape[1])
		dtype = clf_layer.W.dtype
		clf_layer.W.data = np.zeros(w_shape, dtype=dtype)
		clf_layer.b.data = np.zeros(w_shape[0], dtype=dtype)
		initializer(clf_layer.W.data)


	@classmethod
	def prepare(cls, img, size=None):
		size = size or cls.meta.input_size
		if isinstance(size, int):
			size = (size, size)
		return cls.meta.prepare_func(img, size=size)

	@classmethod
	def prepare_back(cls, img):
		img = img.transpose(1,2,0).copy()
		mean = cls.meta.mean
		if isinstance(mean, np.ndarray):
			mean = mean.squeeze()
		img += mean
		img = img[..., ::-1].astype(np.uint8)
		return img

	@abc.abstractmethod
	def __call__(self, X, layer_name=None):
		pass

class ModelWrapper(BaseModel, chainer.Chain):

	class meta(object):
		input_size = 224
		feature_size = None
		classifier_layers = ["output/fc"]
		conv_map_layer = "stage4"
		feature_layer = "pool"

	def __init__(self, model, pooling=PoolingType.Default):
		super(ModelWrapper, self).__init__()
		self.__class__.__name__ = model.__class__.__name__

		with self.init_scope():
			self.wrapped = model
			self.pool = PoolingType.new(pooling)
			delattr(self.wrapped.features, "final_pool")

		if hasattr(model, "meta"):
			self.meta = model.meta

		self.meta.feature_size = self.clf_layer.W.shape[-1]

	@property
	def model_instance(self):
		return self.wrapped

	def load_for_inference(self, *args, path="", **kwargs):
		return super(ModelWrapper, self).load_for_inference(*args, path=f"{path}wrapped/", **kwargs)

	def __call__(self, X, layer_name=None):
		if layer_name is None:
			res = self.wrapped(X)

		elif layer_name == self.meta.conv_map_layer:
			res = self.wrapped.features(X)

		elif layer_name == self.meta.feature_layer:
			conv = self.wrapped.features(X)
			res = self.pool(conv)

		elif layer_name == self.clf_layer_name:
			conv = self.wrapped.features(X)
			feat = self.pool(conv)
			res = self.wrapped.output(feat)

		else:
			raise ValueError(f"Dont know how to compute \"{layer_name}\"!")

		return res


class PretrainedModelMixin(BaseModel):
	CHAINER_PRETRAINED = (
		chainer.links.model.vision.resnet.ResNetLayers,
		chainer.links.model.vision.vgg.VGG16Layers,
		chainer.links.model.vision.googlenet.GoogLeNet,
	)

	@property
	def model_instance(self):
		return self

	def __init__(self, n_classes=1000,
		pooling=PoolingType.Default, pooling_params={}, *args, **kwargs):
		if isinstance(self, PretrainedModelMixin.CHAINER_PRETRAINED):
			super(PretrainedModelMixin, self).__init__(
				pretrained_model=None, *args, **kwargs)
		else:
			super(PretrainedModelMixin, self).__init__(*args, **kwargs)

		if "input_dim" not in pooling_params:
			pooling_params["input_dim"] = self.meta.feature_size

		with self.init_scope():
			self.init_layers(n_classes)
			self.pool = PoolingType.new(pooling, **pooling_params)

	def __call__(self, X, layer_name=None):
		layer_name = layer_name or self.meta.classifier_layers[-1]
		caller = super(PretrainedModelMixin, self).__call__
		activations = caller(X, layers=[layer_name])
		if isinstance(activations, dict):
			activations = activations[layer_name]
		return activations

	@abc.abstractmethod
	def init_layers(self, *args, **kwargs):
		raise NotImplementedError()

	@abc.abstractproperty
	def _links(self):
		raise NotImplementedError()

	@property
	def functions(self):
		return OrderedDict(self._links)

class BaseClassifier(chainer.Chain):
	def __init__(self, model, layer_name=None, loss_func=F.softmax_cross_entropy):
		super(BaseClassifier, self).__init__()
		self.layer_name = layer_name or model.meta.classifier_layers[-1]
		self._loss_func = loss_func

		with self.init_scope():
			self.model = model

	def loss(self, pred, y):
		return self.model.loss(pred, y,
			loss_func=self._loss_func)

	def report(self, **values):
		chainer.report(values, self)
