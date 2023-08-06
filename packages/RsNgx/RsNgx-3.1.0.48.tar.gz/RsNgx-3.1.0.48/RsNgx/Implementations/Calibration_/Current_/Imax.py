from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Imax:
	"""Imax commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("imax", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration:CURRent:IMAX \n
		Snippet: driver.calibration.current.imax.set() \n
		Sets the output current to high value 100 % of Imax during current adjustment. \n
		"""
		self._core.io.write(f'CALibration:CURRent:IMAX')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration:CURRent:IMAX \n
		Snippet: driver.calibration.current.imax.set_with_opc() \n
		Sets the output current to high value 100 % of Imax during current adjustment. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:CURRent:IMAX')
