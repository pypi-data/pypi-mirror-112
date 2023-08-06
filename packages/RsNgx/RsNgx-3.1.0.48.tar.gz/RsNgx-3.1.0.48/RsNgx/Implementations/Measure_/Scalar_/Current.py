from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 5 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def dc(self):
		"""dc commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_dc'):
			from .Current_.Dc import Dc
			self._dc = Dc(self._core, self._base)
		return self._dc
