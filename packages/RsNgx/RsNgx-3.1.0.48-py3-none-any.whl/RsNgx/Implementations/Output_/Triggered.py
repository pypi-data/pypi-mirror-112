from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Triggered:
	"""Triggered commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("triggered", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Triggered_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def behavior(self):
		"""behavior commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_behavior'):
			from .Triggered_.Behavior import Behavior
			self._behavior = Behavior(self._core, self._base)
		return self._behavior
