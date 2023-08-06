from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:BEEPer:WARNing[:IMMediate] \n
		Snippet: driver.system.beeper.warningPy.immediate.set() \n
		Returns a single 'error/warning' beep immediately. \n
		"""
		self._core.io.write(f'SYSTem:BEEPer:WARNing:IMMediate')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:BEEPer:WARNing[:IMMediate] \n
		Snippet: driver.system.beeper.warningPy.immediate.set_with_opc() \n
		Returns a single 'error/warning' beep immediately. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:BEEPer:WARNing:IMMediate')
