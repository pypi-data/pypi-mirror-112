from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Model:
	"""Model commands group definition. 11 total commands, 2 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("model", core, parent)

	@property
	def fname(self):
		"""fname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fname'):
			from .Model_.Fname import Fname
			self._fname = Fname(self._core, self._base)
		return self._fname

	@property
	def current(self):
		"""current commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_current'):
			from .Model_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	def save(self) -> None:
		"""SCPI: BATTery:MODel:SAVE \n
		Snippet: driver.battery.model.save() \n
		Saves the current battery model to a file \n
		"""
		self._core.io.write(f'BATTery:MODel:SAVE')

	def save_with_opc(self) -> None:
		"""SCPI: BATTery:MODel:SAVE \n
		Snippet: driver.battery.model.save_with_opc() \n
		Saves the current battery model to a file \n
		Same as save, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'BATTery:MODel:SAVE')

	def load(self) -> None:
		"""SCPI: BATTery:MODel:LOAD \n
		Snippet: driver.battery.model.load() \n
		Loads a battery model for editing. \n
		"""
		self._core.io.write(f'BATTery:MODel:LOAD')

	def load_with_opc(self) -> None:
		"""SCPI: BATTery:MODel:LOAD \n
		Snippet: driver.battery.model.load_with_opc() \n
		Loads a battery model for editing. \n
		Same as load, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'BATTery:MODel:LOAD')

	def set_transfer(self, arg_0: int) -> None:
		"""SCPI: BATTery:MODel:TRANsfer \n
		Snippet: driver.battery.model.set_transfer(arg_0 = 1) \n
		Transfers the loaded battery model into the channel. \n
			:param arg_0: 1 | 2
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:TRANsfer {param}')

	# noinspection PyTypeChecker
	class DataStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Arg_0: List[int]: Sets the value for battery state of charge (SoC) .
			- Arg_1: List[float]: Sets the value for battery open-circuit voltage (Voc) .
			- Arg_2: List[float]: Sets the value for battery internal resistance (ESR) ."""
		__meta_args_list = [
			ArgStruct('Arg_0', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Arg_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Arg_2', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Arg_0: List[int] = None
			self.Arg_1: List[float] = None
			self.Arg_2: List[float] = None

	def get_data(self) -> DataStruct:
		"""SCPI: BATTery:MODel:DATA \n
		Snippet: value: DataStruct = driver.battery.model.get_data() \n
		Sets or queries the battery model data. \n
			:return: structure: for return value, see the help for DataStruct structure arguments.
		"""
		return self._core.io.query_struct('BATTery:MODel:DATA?', self.__class__.DataStruct())

	def set_data(self, value: DataStruct) -> None:
		"""SCPI: BATTery:MODel:DATA \n
		Snippet: driver.battery.model.set_data(value = DataStruct()) \n
		Sets or queries the battery model data. \n
			:param value: see the help for DataStruct structure arguments.
		"""
		self._core.io.write_struct('BATTery:MODel:DATA', value)

	def get_capacity(self) -> float:
		"""SCPI: BATTery:MODel:CAPacity \n
		Snippet: value: float = driver.battery.model.get_capacity() \n
		Sets or queries the battery model capacity. \n
			:return: arg_0: Sets the battery model capacity.
		"""
		response = self._core.io.query_str('BATTery:MODel:CAPacity?')
		return Conversions.str_to_float(response)

	def set_capacity(self, arg_0: float) -> None:
		"""SCPI: BATTery:MODel:CAPacity \n
		Snippet: driver.battery.model.set_capacity(arg_0 = 1.0) \n
		Sets or queries the battery model capacity. \n
			:param arg_0: Sets the battery model capacity.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:CAPacity {param}')

	def get_isoc(self) -> float:
		"""SCPI: BATTery:MODel:ISOC \n
		Snippet: value: float = driver.battery.model.get_isoc() \n
		Sets or queries the initial state of charge (SoC) of the battery model. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('BATTery:MODel:ISOC?')
		return Conversions.str_to_float(response)

	def set_isoc(self, arg_0: float) -> None:
		"""SCPI: BATTery:MODel:ISOC \n
		Snippet: driver.battery.model.set_isoc(arg_0 = 1.0) \n
		Sets or queries the initial state of charge (SoC) of the battery model. \n
			:param arg_0: Initial state of charge (SoC) for the battery model.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:ISOC {param}')

	def clear(self) -> None:
		"""SCPI: BATTery:MODel:CLEar \n
		Snippet: driver.battery.model.clear() \n
		Clears the current battery model. \n
		"""
		self._core.io.write(f'BATTery:MODel:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: BATTery:MODel:CLEar \n
		Snippet: driver.battery.model.clear_with_opc() \n
		Clears the current battery model. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'BATTery:MODel:CLEar')
