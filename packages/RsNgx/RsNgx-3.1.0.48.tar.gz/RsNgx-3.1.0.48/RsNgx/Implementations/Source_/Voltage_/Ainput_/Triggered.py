from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Triggered:
	"""Triggered commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("triggered", core, parent)

	def get_state(self) -> int or bool:
		"""SCPI: [SOURce]:VOLTage:AINPut:TRIGgered[:STATe] \n
		Snippet: value: int or bool = driver.source.voltage.ainput.triggered.get_state() \n
		Sets or queries the trigger condition of the analog input for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:AINPut:TRIGgered:STATe?')
		return Conversions.str_to_int_or_bool(response)

	def set_state(self, arg_0: int or bool) -> None:
		"""SCPI: [SOURce]:VOLTage:AINPut:TRIGgered[:STATe] \n
		Snippet: driver.source.voltage.ainput.triggered.set_state(arg_0 = 1) \n
		Sets or queries the trigger condition of the analog input for the selected channel. \n
			:param arg_0:
				- OFF: There is no DIO pin that has a mode set to Analog In for the selected channel.
				- 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8: DIO pin/s are enabled with a mode set to Analog In for the selected channel.When DIO pin is enabled with Analog In mode, analog input of the channel assigned to that pin will be enabled when the correct voltage is applied to the DIO pin."""
		param = Conversions.decimal_or_bool_value_to_str(arg_0)
		self._core.io.write(f'SOURce:VOLTage:AINPut:TRIGgered:STATe {param}')
