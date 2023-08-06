from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dvm:
	"""Dvm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dvm", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:VOLTage:DVM[:STATe] \n
		Snippet: value: bool = driver.source.voltage.dvm.get_state() \n
		Sets or queries digital voltmeter measurements. \n
			:return: arg_0: 1 Enables digital voltmeter measurement. 0 Disables digital voltmeter measurement.
		"""
		response = self._core.io.query_str_with_opc('SOURce:VOLTage:DVM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: [SOURce]:VOLTage:DVM[:STATe] \n
		Snippet: driver.source.voltage.dvm.set_state(arg_0 = False) \n
		Sets or queries digital voltmeter measurements. \n
			:param arg_0: 1 Enables digital voltmeter measurement. 0 Disables digital voltmeter measurement.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'SOURce:VOLTage:DVM:STATe {param}')
