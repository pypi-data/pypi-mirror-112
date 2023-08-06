from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	@property
	def protection(self):
		"""protection commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_protection'):
			from .Power_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection
