from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Transfer:
	"""Transfer commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("transfer", core, parent)

	def set(self) -> None:
		"""SCPI: ARBitrary:SEQuence:TRANsfer \n
		Snippet: driver.arbitrary.sequence.transfer.set() \n
		Transfers the defined arbitrary table to the selected channel. \n
		"""
		self._core.io.write(f'ARBitrary:SEQuence:TRANsfer')

	def set_with_opc(self) -> None:
		"""SCPI: ARBitrary:SEQuence:TRANsfer \n
		Snippet: driver.arbitrary.sequence.transfer.set_with_opc() \n
		Transfers the defined arbitrary table to the selected channel. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:SEQuence:TRANsfer')
