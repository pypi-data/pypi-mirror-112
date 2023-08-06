from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def set(self, set_new_value: float, return_min_or_max: enums.MinOrMax = None) -> None:
		"""SCPI: LOG:COUNt \n
		Snippet: driver.log.count.set(set_new_value = 1.0, return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the number of measurement values to be captured. \n
			:param set_new_value: No help available
			:param return_min_or_max: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('set_new_value', set_new_value, DataType.Float), ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		self._core.io.write(f'LOG:COUNt {param}'.rstrip())

	def get(self, return_min_or_max: enums.MinOrMax = None) -> int:
		"""SCPI: LOG:COUNt \n
		Snippet: value: int = driver.log.count.get(return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the number of measurement values to be captured. \n
			:param return_min_or_max: No help available
			:return: result: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		response = self._core.io.query_str(f'LOG:COUNt? {param}'.rstrip())
		return Conversions.str_to_int(response)
