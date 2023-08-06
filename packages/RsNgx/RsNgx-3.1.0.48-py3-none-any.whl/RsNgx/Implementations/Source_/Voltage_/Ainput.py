from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ainput:
	"""Ainput commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ainput", core, parent)

	@property
	def triggered(self):
		"""triggered commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_triggered'):
			from .Ainput_.Triggered import Triggered
			self._triggered = Triggered(self._core, self._base)
		return self._triggered

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:VOLTage:AINPut[:STATe] \n
		Snippet: value: bool = driver.source.voltage.ainput.get_state() \n
		Enables or disables the analog input for the selected channel. \n
			:return: arg_0:
				- 1: Analog input for selected channel is enabled.
				- 0: Analog input for selected channel is disabled."""
		response = self._core.io.query_str('SOURce:VOLTage:AINPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: [SOURce]:VOLTage:AINPut[:STATe] \n
		Snippet: driver.source.voltage.ainput.set_state(arg_0 = False) \n
		Enables or disables the analog input for the selected channel. \n
			:param arg_0:
				- 1: Analog input for selected channel is enabled.
				- 0: Analog input for selected channel is disabled."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SOURce:VOLTage:AINPut:STATe {param}')

	def get_input_py(self) -> str:
		"""SCPI: [SOURce]:VOLTage:AINPut:INPut \n
		Snippet: value: str = driver.source.voltage.ainput.get_input_py() \n
		Sets or queries the analog input mode. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:AINPut:INPut?')
		return trim_str_response(response)

	def set_input_py(self, arg_0: str) -> None:
		"""SCPI: [SOURce]:VOLTage:AINPut:INPut \n
		Snippet: driver.source.voltage.ainput.set_input_py(arg_0 = r1) \n
		Sets or queries the analog input mode. \n
			:param arg_0:
				- VOLT: Voltage mode.
				- CURR: Current mode."""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write(f'SOURce:VOLTage:AINPut:INPut {param}')
