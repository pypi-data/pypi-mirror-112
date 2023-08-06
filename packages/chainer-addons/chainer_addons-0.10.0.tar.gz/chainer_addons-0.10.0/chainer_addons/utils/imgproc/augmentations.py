import numpy as np

from functools import reduce, partial, wraps
from collections.abc import Iterable

from chainercv import transforms as tr

def asarray(func):

	@wraps(func)
	def inner(image, *args, **kw):
		from PIL import Image
		is_pil = isinstance(image, Image.Image)
		if is_pil:
			image = np.asarray(image)
		image = func(image, *args, **kw)
		if is_pil:
			image = Image.fromarray(image)
		return image

	return inner

def crop(image, x,y,w,h):
	return image[:, y: y + h, x: x + w]

@asarray
def random_horizontal_flip(image, threshold=.5, axis=2):
	if np.random.random() < threshold:
		return np.flip(image, axis=axis)
	return image

@asarray
def random_crop(image, crop_size):
	th, tw = crop_size
	c, h, w = image.shape
	th, tw = min(th, h), min(tw, w)
	x = np.random.randint(0, w - tw)
	y = np.random.randint(0, h - th)
	return crop(image, x, y, tw, th)

@asarray
def _center_crop(image, crop_size):
	th, tw = crop_size
	c, h, w = image.shape
	th, tw = min(th, h), min(tw, w)
	x = int((w - tw) / 2.)
	y = int((h - th) / 2.)
	return crop(image, x, y, tw, th)



class Augmentation(object):
	def __init__(self):
		self.augmentations = []

	def __call__(self, image):
		if not self.augmentations: return image
		def call(val, func):
			return func(val)
		return reduce(
			call, self.augmentations,
			image)

	def center_crop(self, size):
		self.augmentations.append(
			partial(_center_crop, crop_size=size))
		return self

	def random_crop(self, size):
		self.augmentations.append(
			partial(random_crop, crop_size=size))
		return self

	def random_horizontal_flip(self, threshold=.5, axis=2):

		self.augmentations.append(
			partial(random_horizontal_flip, threshold=threshold, axis=axis))
		return self
