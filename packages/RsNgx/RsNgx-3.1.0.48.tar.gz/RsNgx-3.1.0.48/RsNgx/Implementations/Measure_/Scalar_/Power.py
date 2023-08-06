from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_max(self) -> float:
		"""SCPI: MEASure[:SCALar]:POWer:MAX \n
		Snippet: value: float = driver.measure.scalar.power.get_max() \n
		Queries the maximum measured output power. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:POWer:MAX?')
		return Conversions.str_to_float(response)

	def get_avg(self) -> float:
		"""SCPI: MEASure[:SCALar]:POWer:AVG \n
		Snippet: value: float = driver.measure.scalar.power.get_avg() \n
		Queries the average measured output power. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:POWer:AVG?')
		return Conversions.str_to_float(response)

	def get_min(self) -> float:
		"""SCPI: MEASure[:SCALar]:POWer:MIN \n
		Snippet: value: float = driver.measure.scalar.power.get_min() \n
		Queries the minimum measured output power. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:POWer:MIN?')
		return Conversions.str_to_float(response)

	def get_statistic(self) -> float:
		"""SCPI: MEASure[:SCALar]:POWer:STATistic \n
		Snippet: value: float = driver.measure.scalar.power.get_statistic() \n
		Queries the power statistics of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:POWer:STATistic?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: MEASure[:SCALar]:POWer \n
		Snippet: value: float = driver.measure.scalar.power.get_value() \n
		Queries the currently emitted power of the selected channel \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:POWer?')
		return Conversions.str_to_float(response)
