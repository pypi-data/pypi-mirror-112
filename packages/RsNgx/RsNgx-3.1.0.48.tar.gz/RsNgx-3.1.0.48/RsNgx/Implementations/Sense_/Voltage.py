from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voltage:
	"""Voltage commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voltage", core, parent)

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_range'):
			from .Voltage_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range
