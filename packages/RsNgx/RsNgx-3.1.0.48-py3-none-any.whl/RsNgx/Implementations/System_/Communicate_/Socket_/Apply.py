from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apply:
	"""Apply commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apply", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:APPLy \n
		Snippet: driver.system.communicate.socket.apply.set() \n
		Apply LAN configuration settings. \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:APPLy')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:APPLy \n
		Snippet: driver.system.communicate.socket.apply.set_with_opc() \n
		Apply LAN configuration settings. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:SOCKet:APPLy')
