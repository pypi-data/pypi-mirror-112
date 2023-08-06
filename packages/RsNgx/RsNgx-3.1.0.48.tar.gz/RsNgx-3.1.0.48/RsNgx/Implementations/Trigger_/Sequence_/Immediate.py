from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 6 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	@property
	def source(self):
		"""source commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Immediate_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source
