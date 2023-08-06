from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Status:
	"""Status commands group definition. 20 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("status", core, parent)

	@property
	def operation(self):
		"""operation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_operation'):
			from .Status_.Operation import Operation
			self._operation = Operation(self._core, self._base)
		return self._operation

	@property
	def questionable(self):
		"""questionable commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_questionable'):
			from .Status_.Questionable import Questionable
			self._questionable = Questionable(self._core, self._base)
		return self._questionable
