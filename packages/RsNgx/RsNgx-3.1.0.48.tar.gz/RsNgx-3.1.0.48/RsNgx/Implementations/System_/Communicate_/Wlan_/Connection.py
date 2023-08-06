from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connection", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:WLAN:CONNection[:STATe] \n
		Snippet: value: bool = driver.system.communicate.wlan.connection.get_state() \n
		Connects or disconnects WLAN to the predefined wireless access point. Available only if option R&S NGP-K102. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:CONNection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:CONNection[:STATe] \n
		Snippet: driver.system.communicate.wlan.connection.set_state(arg_0 = False) \n
		Connects or disconnects WLAN to the predefined wireless access point. Available only if option R&S NGP-K102. \n
			:param arg_0:
				- 1: Connect WLAN to the predefined wireless access point.
				- 0: Disconnect WLAN from the predefined wireless access point."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:CONNection:STATe {param}')
