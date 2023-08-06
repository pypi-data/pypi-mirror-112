from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interval:
	"""Interval commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interval", core, parent)

	def set(self, set_new_value: float, return_min_or_max: enums.MinOrMax = None) -> None:
		"""SCPI: LOG:INTerval \n
		Snippet: driver.log.interval.set(set_new_value = 1.0, return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the data logging measurement interval. The measurement interval describes the time between the recorded
		measurements. \n
			:param set_new_value:
				- numeric value: Measurement interval in the range of 0.008 s to 600 s.
				- MIN | MINimum: Minimum measurement interval is set at 0.008 s.
				- MAX | MAXimum: Maximum measurement interval is set at 600 s.
			:param return_min_or_max: Returns the measurement interval."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('set_new_value', set_new_value, DataType.Float), ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		self._core.io.write(f'LOG:INTerval {param}'.rstrip())

	def get(self, return_min_or_max: enums.MinOrMax = None) -> float:
		"""SCPI: LOG:INTerval \n
		Snippet: value: float = driver.log.interval.get(return_min_or_max = enums.MinOrMax.MAX) \n
		Sets or queries the data logging measurement interval. The measurement interval describes the time between the recorded
		measurements. \n
			:param return_min_or_max: Returns the measurement interval.
			:return: result: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('return_min_or_max', return_min_or_max, DataType.Enum, True))
		response = self._core.io.query_str(f'LOG:INTerval? {param}'.rstrip())
		return Conversions.str_to_float(response)
