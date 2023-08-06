from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	def set(self, set_new_value: float, return_min_or_max: enums.MinOrMax = None) -> None:
		"""SCPI: LOG:DURation \n
		Snippet: driver.log.duration.set(set_new_value = 1.0, return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the duration of the data logging. \n
			:param set_new_value:
				- numeric value: Duration of the data logging captured in the range of 0 s to 3.49*10^5 s.
				- MIN | MINimum: Minimum duration of the data logging captured at 0 s.
				- MAX | MAXimum: Maximum duration of the data logging captured at 3.49*10^5 s.
			:param return_min_or_max: Returns the duration of the data logging."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('set_new_value', set_new_value, DataType.Float), ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		self._core.io.write(f'LOG:DURation {param}'.rstrip())

	def get(self, return_min_or_max: enums.MinOrMax = None) -> int:
		"""SCPI: LOG:DURation \n
		Snippet: value: int = driver.log.duration.get(return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the duration of the data logging. \n
			:param return_min_or_max: Returns the duration of the data logging.
			:return: result: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		response = self._core.io.query_str(f'LOG:DURation? {param}'.rstrip())
		return Conversions.str_to_int(response)
