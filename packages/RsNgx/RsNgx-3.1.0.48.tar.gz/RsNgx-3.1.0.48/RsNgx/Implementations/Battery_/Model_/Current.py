from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_limit'):
			from .Current_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit
