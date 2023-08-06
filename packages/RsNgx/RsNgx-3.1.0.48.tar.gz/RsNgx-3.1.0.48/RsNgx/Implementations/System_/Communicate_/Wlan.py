from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wlan:
	"""Wlan commands group definition. 9 total commands, 2 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wlan", core, parent)

	@property
	def connection(self):
		"""connection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Wlan_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Wlan_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	def get_state(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:WLAN[:STATe] \n
		Snippet: value: bool = driver.system.communicate.wlan.get_state() \n
		Enables or disables WLAN state. Available only if option R&S NGP-K102. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN[:STATe] \n
		Snippet: driver.system.communicate.wlan.set_state(arg_0 = False) \n
		Enables or disables WLAN state. Available only if option R&S NGP-K102. \n
			:param arg_0:
				- 1: Enable WLAN.
				- 0: Disable WLAN."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:STATe {param}')

	def get_ssid(self) -> str:
		"""SCPI: SYSTem:COMMunicate:WLAN:SSID \n
		Snippet: value: str = driver.system.communicate.wlan.get_ssid() \n
		Sets or queries SSID of the access point when wireless interface works as a client. Available only if option R&S NGP-K102. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:SSID?')
		return trim_str_response(response)

	def set_ssid(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:SSID \n
		Snippet: driver.system.communicate.wlan.set_ssid(arg_0 = '1') \n
		Sets or queries SSID of the access point when wireless interface works as a client. Available only if option R&S NGP-K102. \n
			:param arg_0: SSID of access point.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:SSID {param}')

	def set_password(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:PASSword \n
		Snippet: driver.system.communicate.wlan.set_password(arg_0 = '1') \n
		Sets or queries password for WLAN. Available only if option R&S NGP-K102. \n
			:param arg_0: WLAN password.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:PASSword {param}')

	def get_dhcp(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:WLAN:DHCP \n
		Snippet: value: bool = driver.system.communicate.wlan.get_dhcp() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:DHCP?')
		return Conversions.str_to_bool(response)

	def set_dhcp(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:DHCP \n
		Snippet: driver.system.communicate.wlan.set_dhcp(arg_0 = False) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:DHCP {param}')

	def get_ip_address(self) -> str:
		"""SCPI: SYSTem:COMMunicate:WLAN:IPADdress \n
		Snippet: value: str = driver.system.communicate.wlan.get_ip_address() \n
		Queries IP address for WLAN. Available only if option R&S NGP-K102. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:IPADdress?')
		return trim_str_response(response)

	def set_ip_address(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:IPADdress \n
		Snippet: driver.system.communicate.wlan.set_ip_address(arg_0 = '1') \n
		Queries IP address for WLAN. Available only if option R&S NGP-K102. \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:IPADdress {param}')

	def get_mask(self) -> str:
		"""SCPI: SYSTem:COMMunicate:WLAN:MASK \n
		Snippet: value: str = driver.system.communicate.wlan.get_mask() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:MASK?')
		return trim_str_response(response)

	def set_mask(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:MASK \n
		Snippet: driver.system.communicate.wlan.set_mask(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:MASK {param}')

	def get_gateway(self) -> str:
		"""SCPI: SYSTem:COMMunicate:WLAN:GATeway \n
		Snippet: value: str = driver.system.communicate.wlan.get_gateway() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:WLAN:GATeway?')
		return trim_str_response(response)

	def set_gateway(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:WLAN:GATeway \n
		Snippet: driver.system.communicate.wlan.set_gateway(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:WLAN:GATeway {param}')
