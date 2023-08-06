from typing import List

from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arbitrary:
	"""Arbitrary commands group definition. 25 total commands, 6 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arbitrary", core, parent)

	@property
	def block(self):
		"""block commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_block'):
			from .Arbitrary_.Block import Block
			self._block = Block(self._core, self._base)
		return self._block

	@property
	def triggered(self):
		"""triggered commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_triggered'):
			from .Arbitrary_.Triggered import Triggered
			self._triggered = Triggered(self._core, self._base)
		return self._triggered

	@property
	def sequence(self):
		"""sequence commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_sequence'):
			from .Arbitrary_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence

	@property
	def fname(self):
		"""fname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fname'):
			from .Arbitrary_.Fname import Fname
			self._fname = Fname(self._core, self._base)
		return self._fname

	@property
	def behavior(self):
		"""behavior commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_behavior'):
			from .Arbitrary_.Behavior import Behavior
			self._behavior = Behavior(self._core, self._base)
		return self._behavior

	@property
	def priority(self):
		"""priority commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_priority'):
			from .Arbitrary_.Priority import Priority
			self._priority = Priority(self._core, self._base)
		return self._priority

	def get_state(self) -> bool:
		"""SCPI: ARBitrary[:STATe] \n
		Snippet: value: bool = driver.arbitrary.get_state() \n
		Sets or queries the QuickArb function for the previous selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: ARBitrary[:STATe] \n
		Snippet: driver.arbitrary.set_state(arg_0 = False) \n
		Sets or queries the QuickArb function for the previous selected channel. \n
			:param arg_0:
				- 1: QuickArb function is activated.
				- 0: QuickArb function is deactivated."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'ARBitrary:STATe {param}')

	def get_data(self) -> List[float]:
		"""SCPI: ARBitrary:DATA \n
		Snippet: value: List[float] = driver.arbitrary.get_data() \n
		Sets or queries the arbitrary points for the previous selected channel. Max. 1024 arbitrary points can be defined.
		The dwell time between 2 arbitrary points is specified from 1 ms to 60 ms. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('ARBitrary:DATA?')
		return response

	def set_data(self, arg_0: List[float]) -> None:
		"""SCPI: ARBitrary:DATA \n
		Snippet: driver.arbitrary.set_data(arg_0 = [1.1, 2.2, 3.3]) \n
		Sets or queries the arbitrary points for the previous selected channel. Max. 1024 arbitrary points can be defined.
		The dwell time between 2 arbitrary points is specified from 1 ms to 60 ms. \n
			:param arg_0: Voltage and current settings depending on the instrument type. If the interpolation mode is sets to 1, it indicates that the mode is activated. If the interpolation mode is sets to 0, it indicates that the mode is not activated.
		"""
		param = Conversions.list_to_csv_str(arg_0)
		self._core.io.write(f'ARBitrary:DATA {param}')

	def get_repetitions(self) -> int:
		"""SCPI: ARBitrary:REPetitions \n
		Snippet: value: int = driver.arbitrary.get_repetitions() \n
		Sets or queries the repetition rate of the defined arbitrary waveform for the previous selected channel. Up to 65535
		repetitions are possible. If the repetition rate '0' is selected the arbitrary waveform of the previous selected channel
		is repeated infinitely. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:REPetitions?')
		return Conversions.str_to_int(response)

	def set_repetitions(self, arg_0: int) -> None:
		"""SCPI: ARBitrary:REPetitions \n
		Snippet: driver.arbitrary.set_repetitions(arg_0 = 1) \n
		Sets or queries the repetition rate of the defined arbitrary waveform for the previous selected channel. Up to 65535
		repetitions are possible. If the repetition rate '0' is selected the arbitrary waveform of the previous selected channel
		is repeated infinitely. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:REPetitions {param}')

	def clear(self) -> None:
		"""SCPI: ARBitrary:CLEar \n
		Snippet: driver.arbitrary.clear() \n
		Clears the previous defined arbitrary waveform data for the selected channel. \n
		"""
		self._core.io.write(f'ARBitrary:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: ARBitrary:CLEar \n
		Snippet: driver.arbitrary.clear_with_opc() \n
		Clears the previous defined arbitrary waveform data for the selected channel. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:CLEar')

	def save(self) -> None:
		"""SCPI: ARBitrary:SAVE \n
		Snippet: driver.arbitrary.save() \n
		Saves the current arbitrary table to a file (filename specified with method RsNgx.Arbitrary.Fname.set) . \n
		"""
		self._core.io.write(f'ARBitrary:SAVE')

	def save_with_opc(self) -> None:
		"""SCPI: ARBitrary:SAVE \n
		Snippet: driver.arbitrary.save_with_opc() \n
		Saves the current arbitrary table to a file (filename specified with method RsNgx.Arbitrary.Fname.set) . \n
		Same as save, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:SAVE')

	def load(self) -> None:
		"""SCPI: ARBitrary:LOAD \n
		Snippet: driver.arbitrary.load() \n
		Loads an arbitrary table from a file (filename specified with method RsNgx.Arbitrary.Fname.set) \n
		"""
		self._core.io.write(f'ARBitrary:LOAD')

	def load_with_opc(self) -> None:
		"""SCPI: ARBitrary:LOAD \n
		Snippet: driver.arbitrary.load_with_opc() \n
		Loads an arbitrary table from a file (filename specified with method RsNgx.Arbitrary.Fname.set) \n
		Same as load, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ARBitrary:LOAD')

	def set_transfer(self, arg_0: int) -> None:
		"""SCPI: ARBitrary:TRANsfer \n
		Snippet: driver.arbitrary.set_transfer(arg_0 = 1) \n
		Transfers the defined arbitrary table. \n
			:param arg_0: 1
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:TRANsfer {param}')
