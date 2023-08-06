from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HardCopy:
	"""HardCopy commands group definition. 4 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hardCopy", core, parent)

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .HardCopy_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def size(self):
		"""size commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_size'):
			from .HardCopy_.Size import Size
			self._size = Size(self._core, self._base)
		return self._size

	def get_data(self) -> bytes:
		"""SCPI: HCOPy:DATA \n
		Snippet: value: bytes = driver.hardCopy.get_data() \n
		Returns the actual display content (screenshot) . \n
			:return: result: No help available
		"""
		response = self._core.io.query_bin_block('HCOPy:DATA?')
		return response
