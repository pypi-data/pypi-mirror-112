from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umin:
	"""Umin commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umin", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration:AINPut:UMIN \n
		Snippet: driver.calibration.ainput.umin.set() \n
		Sets the output voltage to low value 1 % of Vmax for analog input pin during adjustment. \n
		"""
		self._core.io.write(f'CALibration:AINPut:UMIN')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration:AINPut:UMIN \n
		Snippet: driver.calibration.ainput.umin.set_with_opc() \n
		Sets the output voltage to low value 1 % of Vmax for analog input pin during adjustment. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:AINPut:UMIN')
