from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Protection:
	"""Protection commands group definition. 7 total commands, 2 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("protection", core, parent)

	@property
	def link(self):
		"""link commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_link'):
			from .Protection_.Link import Link
			self._link = Link(self._core, self._base)
		return self._link

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Protection_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:CURRent:PROTection[:STATe] \n
		Snippet: value: bool = driver.source.current.protection.get_state() \n
		Sets or queries the OCP state. \n
			:return: arg_0: 1 Activates the OCP state. 0 deactivates the OCP state.
		"""
		response = self._core.io.query_str('SOURce:CURRent:PROTection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection[:STATe] \n
		Snippet: driver.source.current.protection.set_state(arg_0 = False) \n
		Sets or queries the OCP state. \n
			:param arg_0: 1 Activates the OCP state. 0 deactivates the OCP state.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SOURce:CURRent:PROTection:STATe {param}')

	def set_unlink(self, arg_0: int) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:UNLink \n
		Snippet: driver.source.current.protection.set_unlink(arg_0 = 1) \n
		Unlink fuse linking from the other channel (Ch1 or Ch2) . See Example 'Configuring fuses'. \n
			:param arg_0: 1 | 2
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SOURce:CURRent:PROTection:UNLink {param}')

	def get_tripped(self) -> bool:
		"""SCPI: [SOURce]:CURRent:PROTection:TRIPped \n
		Snippet: value: bool = driver.source.current.protection.get_tripped() \n
		Queries the OCP state of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('SOURce:CURRent:PROTection:TRIPped?')
		return Conversions.str_to_bool(response)

	def clear(self) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:CLEar \n
		Snippet: driver.source.current.protection.clear() \n
		Resets the OCP state of the selected channel. If an OCP event has occurred before, the reset also erases the message on
		the display. \n
		"""
		self._core.io.write(f'SOURce:CURRent:PROTection:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:CLEar \n
		Snippet: driver.source.current.protection.clear_with_opc() \n
		Resets the OCP state of the selected channel. If an OCP event has occurred before, the reset also erases the message on
		the display. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:CURRent:PROTection:CLEar')
