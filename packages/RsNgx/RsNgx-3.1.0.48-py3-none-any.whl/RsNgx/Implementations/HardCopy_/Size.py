from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Size:
	"""Size commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("size", core, parent)

	def get_x(self) -> int:
		"""SCPI: HCOPy:SIZE:X \n
		Snippet: value: int = driver.hardCopy.size.get_x() \n
		Returns the horizontal dimension of the screenshots. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('HCOPy:SIZE:X?')
		return Conversions.str_to_int(response)

	def get_y(self) -> int:
		"""SCPI: HCOPy:SIZE:Y \n
		Snippet: value: int = driver.hardCopy.size.get_y() \n
		Returns the vertical dimension of the screenshots. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('HCOPy:SIZE:Y?')
		return Conversions.str_to_int(response)
