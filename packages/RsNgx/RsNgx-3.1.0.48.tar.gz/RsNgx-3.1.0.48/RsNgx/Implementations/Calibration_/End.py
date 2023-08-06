from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class End:
	"""End commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("end", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration:END \n
		Snippet: driver.calibration.end.set() \n
		Ends the channel adjustment. \n
		"""
		self._core.io.write(f'CALibration:END')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration:END \n
		Snippet: driver.calibration.end.set_with_opc() \n
		Ends the channel adjustment. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:END')
