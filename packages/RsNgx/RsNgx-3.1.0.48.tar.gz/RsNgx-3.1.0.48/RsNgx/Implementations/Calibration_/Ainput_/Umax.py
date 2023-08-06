from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umax:
	"""Umax commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umax", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration:AINPut:UMAX \n
		Snippet: driver.calibration.ainput.umax.set() \n
		Sets output voltage to high value 100 % of Vmax for analog input pin during adjustment. \n
		"""
		self._core.io.write(f'CALibration:AINPut:UMAX')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration:AINPut:UMAX \n
		Snippet: driver.calibration.ainput.umax.set_with_opc() \n
		Sets output voltage to high value 100 % of Vmax for analog input pin during adjustment. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:AINPut:UMAX')
