from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umax:
	"""Umax commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umax", core, parent)

	def set(self) -> None:
		"""SCPI: CALibration:VOLTage:UMAX \n
		Snippet: driver.calibration.voltage.umax.set() \n
		Sets the output voltage to high value 100 % of Vmax during voltage adjustment. \n
		"""
		self._core.io.write(f'CALibration:VOLTage:UMAX')

	def set_with_opc(self) -> None:
		"""SCPI: CALibration:VOLTage:UMAX \n
		Snippet: driver.calibration.voltage.umax.set_with_opc() \n
		Sets the output voltage to high value 100 % of Vmax during voltage adjustment. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:VOLTage:UMAX')
