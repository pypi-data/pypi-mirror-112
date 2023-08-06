from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scalar:
	"""Scalar commands group definition. 20 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scalar", core, parent)

	@property
	def voltage(self):
		"""voltage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_voltage'):
			from .Scalar_.Voltage import Voltage
			self._voltage = Voltage(self._core, self._base)
		return self._voltage

	@property
	def current(self):
		"""current commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_current'):
			from .Scalar_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def energy(self):
		"""energy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_energy'):
			from .Scalar_.Energy import Energy
			self._energy = Energy(self._core, self._base)
		return self._energy

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_power'):
			from .Scalar_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def statistic(self):
		"""statistic commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_statistic'):
			from .Scalar_.Statistic import Statistic
			self._statistic = Statistic(self._core, self._base)
		return self._statistic
