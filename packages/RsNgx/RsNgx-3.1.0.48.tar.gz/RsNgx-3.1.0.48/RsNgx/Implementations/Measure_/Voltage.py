from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voltage:
	"""Voltage commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voltage", core, parent)

	def get_dvm(self) -> float:
		"""SCPI: MEASure:VOLTage:DVM \n
		Snippet: value: float = driver.measure.voltage.get_dvm() \n
		Queries the voltmeter measurement (if DVM is enabled) . The DVM is available only with NGU201 model equipped with R&S
		NGU-K104 (P/N: 3663.0390.02) . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:VOLTage:DVM?')
		return Conversions.str_to_float(response)
