from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dc:
	"""Dc commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dc", core, parent)

	def get_max(self) -> float:
		"""SCPI: MEASure[:SCALar]:CURRent[:DC]:MAX \n
		Snippet: value: float = driver.measure.scalar.current.dc.get_max() \n
		Queries the maximum measured output current. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:CURRent:DC:MAX?')
		return Conversions.str_to_float(response)

	def get_avg(self) -> float:
		"""SCPI: MEASure[:SCALar]:CURRent[:DC]:AVG \n
		Snippet: value: float = driver.measure.scalar.current.dc.get_avg() \n
		Queries the average measured output current. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:CURRent:DC:AVG?')
		return Conversions.str_to_float(response)

	def get_min(self) -> float:
		"""SCPI: MEASure[:SCALar]:CURRent[:DC]:MIN \n
		Snippet: value: float = driver.measure.scalar.current.dc.get_min() \n
		Queries the minimum measured output power. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:CURRent:DC:MIN?')
		return Conversions.str_to_float(response)

	def get_statistic(self) -> float:
		"""SCPI: MEASure[:SCALar]:CURRent[:DC]:STATistic \n
		Snippet: value: float = driver.measure.scalar.current.dc.get_statistic() \n
		Queries the current statistics of the selected channel \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:CURRent:DC:STATistic?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: MEASure[:SCALar]:CURRent[:DC] \n
		Snippet: value: float = driver.measure.scalar.current.dc.get_value() \n
		Queries the currently measured current of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:CURRent:DC?')
		return Conversions.str_to_float(response)
