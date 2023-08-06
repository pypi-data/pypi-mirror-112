from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vnc:
	"""Vnc commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vnc", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SYSTem:VNC:STATe \n
		Snippet: value: bool = driver.system.vnc.get_state() \n
		Enables or disables VNC state. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:VNC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:VNC:STATe \n
		Snippet: driver.system.vnc.set_state(arg_0 = False) \n
		Enables or disables VNC state. \n
			:param arg_0:
				- 1: Enable VNC.
				- 0: Disable VNC."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:VNC:STATe {param}')

	def get_port(self) -> int:
		"""SCPI: SYSTem:VNC:PORT \n
		Snippet: value: int = driver.system.vnc.get_port() \n
		Sets or queries the VNC port number. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:VNC:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, arg_0: int) -> None:
		"""SCPI: SYSTem:VNC:PORT \n
		Snippet: driver.system.vnc.set_port(arg_0 = 1) \n
		Sets or queries the VNC port number. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SYSTem:VNC:PORT {param}')
