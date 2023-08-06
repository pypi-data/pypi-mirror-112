from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 5 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	@property
	def transfer(self):
		"""transfer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_transfer'):
			from .Sequence_.Transfer import Transfer
			self._transfer = Transfer(self._core, self._base)
		return self._transfer

	@property
	def behavior(self):
		"""behavior commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_behavior'):
			from .Sequence_.Behavior import Behavior
			self._behavior = Behavior(self._core, self._base)
		return self._behavior

	def get_repetitions(self) -> int:
		"""SCPI: ARBitrary:SEQuence:REPetitions \n
		Snippet: value: int = driver.arbitrary.sequence.get_repetitions() \n
		Sets or queries the number of repetitions of the arbitrary sequence \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:SEQuence:REPetitions?')
		return Conversions.str_to_int(response)

	def set_repetitions(self, arg_0: int) -> None:
		"""SCPI: ARBitrary:SEQuence:REPetitions \n
		Snippet: driver.arbitrary.sequence.set_repetitions(arg_0 = 1) \n
		Sets or queries the number of repetitions of the arbitrary sequence \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:SEQuence:REPetitions {param}')

	def get_endpoint(self) -> int:
		"""SCPI: ARBitrary:SEQuence:ENDPoint \n
		Snippet: value: int = driver.arbitrary.sequence.get_endpoint() \n
		Queries the total number of points of the arbitrary sequence. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('ARBitrary:SEQuence:ENDPoint?')
		return Conversions.str_to_int(response)

	def clear(self) -> None:
		"""SCPI: ARBitrary:SEQuence:CLEar \n
		Snippet: driver.arbitrary.sequence.clear() \n
		Clears the arbitrary sequence. \n
		"""
		self._core.io.write(f'ARBitrary:SEQuence:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: ARBitrary:SEQuence:CLEar \n
		Snippet: driver.arbitrary.sequence.clear_with_opc() \n
		Clears the arbitrary sequence. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:SEQuence:CLEar')
