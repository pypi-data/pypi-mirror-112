from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Socket:
	"""Socket commands group definition. 7 total commands, 2 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("socket", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Socket_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def discard(self):
		"""discard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_discard'):
			from .Socket_.Discard import Discard
			self._discard = Discard(self._core, self._base)
		return self._discard

	def get_dhcp(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:SOCKet:DHCP \n
		Snippet: value: bool = driver.system.communicate.socket.get_dhcp() \n
		Sets the LAN interface mode. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:DHCP?')
		return Conversions.str_to_bool(response)

	def set_dhcp(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:DHCP \n
		Snippet: driver.system.communicate.socket.set_dhcp(arg_0 = False) \n
		Sets the LAN interface mode. \n
			:param arg_0:
				- 1: DHCP is enabled.Automatic IP address from DHCP server.
				- 0: DHCP is disabled.Manually set IP address."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:DHCP {param}')

	def get_ip_address(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:IPADdress \n
		Snippet: value: str = driver.system.communicate.socket.get_ip_address() \n
		Sets or queries IP address of the LAN interface. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:IPADdress?')
		return trim_str_response(response)

	def set_ip_address(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:IPADdress \n
		Snippet: driver.system.communicate.socket.set_ip_address(arg_0 = '1') \n
		Sets or queries IP address of the LAN interface. \n
			:param arg_0: IP address.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:IPADdress {param}')

	def get_mask(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MASK \n
		Snippet: value: str = driver.system.communicate.socket.get_mask() \n
		Sets or queries the subnet mask for LAN. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:MASK?')
		return trim_str_response(response)

	def set_mask(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MASK \n
		Snippet: driver.system.communicate.socket.set_mask(arg_0 = '1') \n
		Sets or queries the subnet mask for LAN. \n
			:param arg_0: Subnet address.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:MASK {param}')

	def get_gateway(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:GATeway \n
		Snippet: value: str = driver.system.communicate.socket.get_gateway() \n
		Sets or queries gateway for LAN. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:GATeway?')
		return trim_str_response(response)

	def set_gateway(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:GATeway \n
		Snippet: driver.system.communicate.socket.set_gateway(arg_0 = '1') \n
		Sets or queries gateway for LAN. \n
			:param arg_0: Gateway address.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:GATeway {param}')

	def reset(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:RESet \n
		Snippet: driver.system.communicate.socket.reset() \n
		Resets LAN settings. \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:RESet \n
		Snippet: driver.system.communicate.socket.reset_with_opc() \n
		Resets LAN settings. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:SOCKet:RESet')
