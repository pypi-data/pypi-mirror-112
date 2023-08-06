from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voc:
	"""Voc commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voc", core, parent)

	def get_full(self) -> float:
		"""SCPI: BATTery:SIMulator:VOC:FULL \n
		Snippet: value: float = driver.battery.simulator.voc.get_full() \n
		Queries the open circuit voltage (Voc) for full SoC, i.e SoC = 100 %. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:VOC:FULL?')
		return Conversions.str_to_float(response)

	def get_empty(self) -> float:
		"""SCPI: BATTery:SIMulator:VOC:EMPTy \n
		Snippet: value: float = driver.battery.simulator.voc.get_empty() \n
		Queries the open circuit voltage (Voc) for empty SoC, i.e SoC = 0 %. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:VOC:EMPTy?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: BATTery:SIMulator:VOC \n
		Snippet: value: float = driver.battery.simulator.voc.get_value() \n
		Queries the open circuit voltage (Voc) . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:VOC?')
		return Conversions.str_to_float(response)
