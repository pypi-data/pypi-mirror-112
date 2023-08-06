from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	@property
	def dio(self):
		"""dio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dio'):
			from .Select_.Dio import Dio
			self._dio = Dio(self._core, self._base)
		return self._dio
