from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Local:
	"""Local commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("local", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:LOCal \n
		Snippet: driver.system.local.set() \n
		Sets the system to front panel control. The front panel control is unlocked. \n
		"""
		self._core.io.write(f'SYSTem:LOCal')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:LOCal \n
		Snippet: driver.system.local.set_with_opc() \n
		Sets the system to front panel control. The front panel control is unlocked. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:LOCal')
