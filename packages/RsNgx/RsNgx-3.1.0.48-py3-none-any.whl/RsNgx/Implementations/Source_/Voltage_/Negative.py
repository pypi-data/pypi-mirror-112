from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Negative:
	"""Negative commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("negative", core, parent)

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Negative_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level
