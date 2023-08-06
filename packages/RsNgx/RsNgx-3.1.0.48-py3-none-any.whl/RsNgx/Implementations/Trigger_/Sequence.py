from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 6 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	@property
	def immediate(self):
		"""immediate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_immediate'):
			from .Sequence_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate
