from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Protection:
	"""Protection commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("protection", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:VOLTage:PROTection[:STATe] \n
		Snippet: value: bool = driver.source.voltage.protection.get_state() \n
		Sets or queries the OVP state of the previous selected channel. \n
			:return: en: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:PROTection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, en: bool) -> None:
		"""SCPI: [SOURce]:VOLTage:PROTection[:STATe] \n
		Snippet: driver.source.voltage.protection.set_state(en = False) \n
		Sets or queries the OVP state of the previous selected channel. \n
			:param en:
				- 0: OVP is deactivated
				- 1: OVP is activated"""
		param = Conversions.bool_to_str(en)
		self._core.io.write(f'SOURce:VOLTage:PROTection:STATe {param}')

	def get_level(self) -> float:
		"""SCPI: [SOURce]:VOLTage:PROTection:LEVel \n
		Snippet: value: float = driver.source.voltage.protection.get_level() \n
		Sets or queries the overvoltage protection value of the selected channel. \n
			:return: voltage_protection: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:PROTection:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, voltage_protection: float) -> None:
		"""SCPI: [SOURce]:VOLTage:PROTection:LEVel \n
		Snippet: driver.source.voltage.protection.set_level(voltage_protection = 1.0) \n
		Sets or queries the overvoltage protection value of the selected channel. \n
			:param voltage_protection:
				- numeric value: Numeric value for the overvoltage protection value in V.
				- MIN | MINimum: Minimum value for the overvoltage protection value at 0.000 V.
				- MAX | MAXimum: Maximum value for the overvoltage protection value at 64.050 V."""
		param = Conversions.decimal_value_to_str(voltage_protection)
		self._core.io.write(f'SOURce:VOLTage:PROTection:LEVel {param}')

	def get_tripped(self) -> bool:
		"""SCPI: [SOURce]:VOLTage:PROTection:TRIPped \n
		Snippet: value: bool = driver.source.voltage.protection.get_tripped() \n
		Queries the OVP state of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:PROTection:TRIPped?')
		return Conversions.str_to_bool(response)

	def clear(self) -> None:
		"""SCPI: [SOURce]:VOLTage:PROTection:CLEar \n
		Snippet: driver.source.voltage.protection.clear() \n
		Resets the OVP state of the selected channel. If an OVP event has occurred before, the reset also erases the message on
		the display. \n
		"""
		self._core.io.write(f'SOURce:VOLTage:PROTection:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: [SOURce]:VOLTage:PROTection:CLEar \n
		Snippet: driver.source.voltage.protection.clear_with_opc() \n
		Resets the OVP state of the selected channel. If an OVP event has occurred before, the reset also erases the message on
		the display. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:VOLTage:PROTection:CLEar')
