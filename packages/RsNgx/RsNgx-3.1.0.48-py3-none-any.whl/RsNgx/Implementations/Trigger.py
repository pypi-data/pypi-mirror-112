from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 14 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def enable(self):
		"""enable commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Trigger_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def direction(self):
		"""direction commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_direction'):
			from .Trigger_.Direction import Direction
			self._direction = Direction(self._core, self._base)
		return self._direction

	@property
	def logic(self):
		"""logic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_logic'):
			from .Trigger_.Logic import Logic
			self._logic = Logic(self._core, self._base)
		return self._logic

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Trigger_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def condition(self):
		"""condition commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_condition'):
			from .Trigger_.Condition import Condition
			self._condition = Condition(self._core, self._base)
		return self._condition

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Trigger_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def sequence(self):
		"""sequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Trigger_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence
