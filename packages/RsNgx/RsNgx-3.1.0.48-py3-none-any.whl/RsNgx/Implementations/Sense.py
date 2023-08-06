from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sense:
	"""Sense commands group definition. 7 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sense", core, parent)

	@property
	def current(self):
		"""current commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_current'):
			from .Sense_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def voltage(self):
		"""voltage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_voltage'):
			from .Sense_.Voltage import Voltage
			self._voltage = Voltage(self._core, self._base)
		return self._voltage

	@property
	def nplCycles(self):
		"""nplCycles commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nplCycles'):
			from .Sense_.NplCycles import NplCycles
			self._nplCycles = NplCycles(self._core, self._base)
		return self._nplCycles
