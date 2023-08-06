from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tripped:
	"""Tripped commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tripped", core, parent)

	def clear(self) -> None:
		"""SCPI: FUSE:TRIPped:CLEar \n
		Snippet: driver.fuse.tripped.clear() \n
		Resets the OCP state of the selected channel. If an OCP event has occurred before, the reset also erases the message on
		the display. \n
		"""
		self._core.io.write(f'FUSE:TRIPped:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: FUSE:TRIPped:CLEar \n
		Snippet: driver.fuse.tripped.clear_with_opc() \n
		Resets the OCP state of the selected channel. If an OCP event has occurred before, the reset also erases the message on
		the display. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'FUSE:TRIPped:CLEar')

	def get_value(self) -> bool:
		"""SCPI: FUSE:TRIPped \n
		Snippet: value: bool = driver.fuse.tripped.get_value() \n
		Queries the OCP state of the selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('FUSE:TRIPped?')
		return Conversions.str_to_bool(response)
