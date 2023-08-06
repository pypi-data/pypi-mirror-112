from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dio:
	"""Dio commands group definition. 7 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dio", core, parent)

	@property
	def fault(self):
		"""fault commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_fault'):
			from .Dio_.Fault import Fault
			self._fault = Fault(self._core, self._base)
		return self._fault

	@property
	def output(self):
		"""output commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Dio_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output
