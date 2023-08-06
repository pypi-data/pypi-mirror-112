from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	@property
	def increment(self):
		"""increment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_increment'):
			from .Step_.Increment import Increment
			self._increment = Increment(self._core, self._base)
		return self._increment
