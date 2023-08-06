from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Window:
	"""Window commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("window", core, parent)

	@property
	def text(self):
		"""text commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_text'):
			from .Window_.Text import Text
			self._text = Text(self._core, self._base)
		return self._text
