from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 41 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	@property
	def current(self):
		"""current commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .Source_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def voltage(self):
		"""voltage commands group. 7 Sub-classes, 1 commands."""
		if not hasattr(self, '_voltage'):
			from .Source_.Voltage import Voltage
			self._voltage = Voltage(self._core, self._base)
		return self._voltage

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Source_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def protection(self):
		"""protection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protection'):
			from .Source_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection

	@property
	def alimit(self):
		"""alimit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alimit'):
			from .Source_.Alimit import Alimit
			self._alimit = Alimit(self._core, self._base)
		return self._alimit

	@property
	def resistance(self):
		"""resistance commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_resistance'):
			from .Source_.Resistance import Resistance
			self._resistance = Resistance(self._core, self._base)
		return self._resistance

	@property
	def modulation(self):
		"""modulation commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Source_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def priority(self):
		"""priority commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_priority'):
			from .Source_.Priority import Priority
			self._priority = Priority(self._core, self._base)
		return self._priority
