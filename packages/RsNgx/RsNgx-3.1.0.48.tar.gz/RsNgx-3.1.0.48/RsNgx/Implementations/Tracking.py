from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tracking:
	"""Tracking commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tracking", core, parent)

	@property
	def enable(self):
		"""enable commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Tracking_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable
