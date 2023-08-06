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
		"""SCPI: MEASure[:SCALar][:VOLTage][:DC]:MAX \n
		Snippet: value: float = driver.measure.scalar.voltage.dc.get_max() \n
		Queries the maximum measured output voltage. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:VOLTage:DC:MAX?')
		return Conversions.str_to_float(response)

	def get_avg(self) -> float:
		"""SCPI: MEASure[:SCALar][:VOLTage][:DC]:AVG \n
		Snippet: value: float = driver.measure.scalar.voltage.dc.get_avg() \n
		Queries the average measured output voltage. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:VOLTage:DC:AVG?')
		return Conversions.str_to_float(response)

	def get_min(self) -> float:
		"""SCPI: MEASure[:SCALar][:VOLTage][:DC]:MIN \n
		Snippet: value: float = driver.measure.scalar.voltage.dc.get_min() \n
		Queries the minimum measured output voltage. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:VOLTage:DC:MIN?')
		return Conversions.str_to_float(response)

	def get_statistic(self) -> float:
		"""SCPI: MEASure[:SCALar][:VOLTage][:DC]:STATistic \n
		Snippet: value: float = driver.measure.scalar.voltage.dc.get_statistic() \n
		Queries the voltage statistics of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:VOLTage:DC:STATistic?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: MEASure[:SCALar][:VOLTage][:DC] \n
		Snippet: value: float = driver.measure.scalar.voltage.dc.get_value() \n
		Queries the currently measured voltage of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:VOLTage:DC?')
		return Conversions.str_to_float(response)
