from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Block:
	"""Block commands group definition. 6 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("block", core, parent)

	@property
	def fname(self):
		"""fname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fname'):
			from .Block_.Fname import Fname
			self._fname = Fname(self._core, self._base)
		return self._fname

	def get_data(self) -> List[float]:
		"""SCPI: ARBitrary:BLOCk:DATA \n
		Snippet: value: List[float] = driver.arbitrary.block.get_data() \n
		Define the data points for a whole block. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('ARBitrary:BLOCk:DATA?')
		return response

	def set_data(self, arg_0: List[float]) -> None:
		"""SCPI: ARBitrary:BLOCk:DATA \n
		Snippet: driver.arbitrary.block.set_data(arg_0 = [1.1, 2.2, 3.3]) \n
		Define the data points for a whole block. \n
			:param arg_0: Voltage and current settings depending on the instrument type. If the interpolation mode is sets to 1, it indicates that the mode is activated. If the interpolation mode is sets to 0, it indicates that the mode is not activated.
		"""
		param = Conversions.list_to_csv_str(arg_0)
		self._core.io.write(f'ARBitrary:BLOCk:DATA {param}')

	def get_repetitions(self) -> int:
		"""SCPI: ARBitrary:BLOCk:REPetitions \n
		Snippet: value: int = driver.arbitrary.block.get_repetitions() \n
		Sets or queries the number of repetitions of the block of arbitrary data. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:BLOCk:REPetitions?')
		return Conversions.str_to_int(response)

	def set_repetitions(self, arg_0: int) -> None:
		"""SCPI: ARBitrary:BLOCk:REPetitions \n
		Snippet: driver.arbitrary.block.set_repetitions(arg_0 = 1) \n
		Sets or queries the number of repetitions of the block of arbitrary data. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:BLOCk:REPetitions {param}')

	def get_endpoint(self) -> int:
		"""SCPI: ARBitrary:BLOCk:ENDPoint \n
		Snippet: value: int = driver.arbitrary.block.get_endpoint() \n
		Queries the number of data points of the block of arbitrary data. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('ARBitrary:BLOCk:ENDPoint?')
		return Conversions.str_to_int(response)

	def clear(self) -> None:
		"""SCPI: ARBitrary:BLOCk:CLEar \n
		Snippet: driver.arbitrary.block.clear() \n
		Clears a file selected for the block under channel arbitrary settings. See also method RsNgx.Arbitrary.Block.value. \n
		"""
		self._core.io.write(f'ARBitrary:BLOCk:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: ARBitrary:BLOCk:CLEar \n
		Snippet: driver.arbitrary.block.clear_with_opc() \n
		Clears a file selected for the block under channel arbitrary settings. See also method RsNgx.Arbitrary.Block.value. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:BLOCk:CLEar')

	def get_value(self) -> int:
		"""SCPI: ARBitrary:BLOCk \n
		Snippet: value: int = driver.arbitrary.block.get_value() \n
		Select individual block between 1 to 8 in an arbitrary sequence. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:BLOCk?')
		return Conversions.str_to_int(response)

	def set_value(self, arg_0: int) -> None:
		"""SCPI: ARBitrary:BLOCk \n
		Snippet: driver.arbitrary.block.set_value(arg_0 = 1) \n
		Select individual block between 1 to 8 in an arbitrary sequence. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:BLOCk {param}')
