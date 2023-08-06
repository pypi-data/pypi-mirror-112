from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RwLock:
	"""RwLock commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rwLock", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:RWLock \n
		Snippet: driver.system.rwLock.set() \n
		Sets the system to remote state. The front panel control is locked. You are only able to unlock the front panel control
		via SCPI command SYSTem:LOCal. \n
		"""
		self._core.io.write(f'SYSTem:RWLock')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:RWLock \n
		Snippet: driver.system.rwLock.set_with_opc() \n
		Sets the system to remote state. The front panel control is locked. You are only able to unlock the front panel control
		via SCPI command SYSTem:LOCal. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:RWLock')
