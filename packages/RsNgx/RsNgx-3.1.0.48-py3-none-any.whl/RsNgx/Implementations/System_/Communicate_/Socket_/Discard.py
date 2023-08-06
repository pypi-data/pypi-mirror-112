from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Discard:
	"""Discard commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("discard", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:DISCard \n
		Snippet: driver.system.communicate.socket.discard.set() \n
		Discards LAN settings. \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:DISCard')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:DISCard \n
		Snippet: driver.system.communicate.socket.discard.set_with_opc() \n
		Discards LAN settings. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:SOCKet:DISCard')
