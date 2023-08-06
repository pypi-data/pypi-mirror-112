import numpy as np

from chainercv import transforms as tr
from collections.abc import Iterable


class ChainerCV2Prepare(object):


	def __init__(self, size, *, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
		super(ChainerCV2Prepare, self).__init__()
		self.size = size
		self.mean = np.array(mean, dtype=np.float32).reshape(-1, 1, 1)
		self.std = np.array(std, dtype=np.float32).reshape(-1, 1, 1)


	def _size(self, size):
		size = self.size if size is None else size
		if isinstance(size, Iterable):
			size = min(size)
		return size

	def __call__(self, im, size=None, *args, **kwargs):

		_im = im.transpose(2, 0, 1)
		_im = _im.astype(np.float32) / 255.0
		_im = tr.scale(_im, self._size(size), interpolation=2)

		_im -= self.mean
		_im /= self.std

		return _im
