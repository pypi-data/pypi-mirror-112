from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lan:
	"""Lan commands group definition. 10 total commands, 2 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lan", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Lan_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def discard(self):
		"""discard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_discard'):
			from .Lan_.Discard import Discard
			self._discard = Discard(self._core, self._base)
		return self._discard

	def get_dhcp(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:LAN:DHCP \n
		Snippet: value: bool = driver.system.communicate.lan.get_dhcp() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:DHCP?')
		return Conversions.str_to_bool(response)

	def set_dhcp(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:DHCP \n
		Snippet: driver.system.communicate.lan.set_dhcp(arg_0 = False) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:LAN:DHCP {param}')

	def get_address(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:ADDRess \n
		Snippet: value: str = driver.system.communicate.lan.get_address() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:ADDRess?')
		return trim_str_response(response)

	def set_address(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:ADDRess \n
		Snippet: driver.system.communicate.lan.set_address(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:LAN:ADDRess {param}')

	def get_smask(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:SMASk \n
		Snippet: value: str = driver.system.communicate.lan.get_smask() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:SMASk?')
		return trim_str_response(response)

	def set_smask(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:SMASk \n
		Snippet: driver.system.communicate.lan.set_smask(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:LAN:SMASk {param}')

	def get_dgateway(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:DGATeway \n
		Snippet: value: str = driver.system.communicate.lan.get_dgateway() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:DGATeway?')
		return trim_str_response(response)

	def set_dgateway(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:DGATeway \n
		Snippet: driver.system.communicate.lan.set_dgateway(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:LAN:DGATeway {param}')

	def get_hostname(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:HOSTname \n
		Snippet: value: str = driver.system.communicate.lan.get_hostname() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, arg_0: str) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:HOSTname \n
		Snippet: driver.system.communicate.lan.set_hostname(arg_0 = '1') \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'SYSTem:COMMunicate:LAN:HOSTname {param}')

	def get_mac(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:MAC \n
		Snippet: value: str = driver.system.communicate.lan.get_mac() \n
		No command help available \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:MAC?')
		return trim_str_response(response)

	def reset(self) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:RESet \n
		Snippet: driver.system.communicate.lan.reset() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:LAN:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: SYSTem:COMMunicate:LAN:RESet \n
		Snippet: driver.system.communicate.lan.reset_with_opc() \n
		No command help available \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:LAN:RESet')

	def get_edited(self) -> str:
		"""SCPI: SYSTem:COMMunicate:LAN:EDITed \n
		Snippet: value: str = driver.system.communicate.lan.get_edited() \n
		No command help available \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:LAN:EDITed?')
		return trim_str_response(response)
