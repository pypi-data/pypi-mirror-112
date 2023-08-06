from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Isummary:
	"""Isummary commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isummary", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Isummary_.Event import Event
			self._event = Event(self._core, self._base)
		return self._event

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Isummary_.Condition import Condition
			self._condition = Condition(self._core, self._base)
		return self._condition

	@property
	def ptransition(self):
		"""ptransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransition'):
			from .Isummary_.Ptransition import Ptransition
			self._ptransition = Ptransition(self._core, self._base)
		return self._ptransition

	@property
	def ntransition(self):
		"""ntransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransition'):
			from .Isummary_.Ntransition import Ntransition
			self._ntransition = Ntransition(self._core, self._base)
		return self._ntransition

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Isummary_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable
