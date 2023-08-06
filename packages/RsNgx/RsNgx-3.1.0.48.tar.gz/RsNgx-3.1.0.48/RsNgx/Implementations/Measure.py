from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measure:
	"""Measure commands group definition. 21 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("measure", core, parent)

	@property
	def scalar(self):
		"""scalar commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_scalar'):
			from .Measure_.Scalar import Scalar
			self._scalar = Scalar(self._core, self._base)
		return self._scalar

	@property
	def voltage(self):
		"""voltage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_voltage'):
			from .Measure_.Voltage import Voltage
			self._voltage = Voltage(self._core, self._base)
		return self._voltage
