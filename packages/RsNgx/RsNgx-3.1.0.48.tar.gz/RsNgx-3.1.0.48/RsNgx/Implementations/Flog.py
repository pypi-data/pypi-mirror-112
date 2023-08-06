from typing import List

from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Flog:
	"""Flog commands group definition. 8 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("flog", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_file'):
			from .Flog_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def get_state(self) -> bool:
		"""SCPI: FLOG[:STATe] \n
		Snippet: value: bool = driver.flog.get_state() \n
		Sets or queries the FastLog state. \n
			:return: arg_0: 1 Enables the FastLog state. 0 Disables the FastLog state.
		"""
		response = self._core.io.query_str('FLOG:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: FLOG[:STATe] \n
		Snippet: driver.flog.set_state(arg_0 = False) \n
		Sets or queries the FastLog state. \n
			:param arg_0: 1 Enables the FastLog state. 0 Disables the FastLog state.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'FLOG:STATe {param}')

	def get_data(self) -> List[float]:
		"""SCPI: FLOG:DATA \n
		Snippet: value: List[float] = driver.flog.get_data() \n
		Queries FastLog data as a block. The block is returned in the binary format starting in the sequence of voltage followed
		by current measurements, i.e. V, I, V, I, .... The R&S NGU accepts the line message EOI and/or the ASCII character NL
		(0Ah) as an indication that data transmission has been completed The binary data stream must be concluded with EOI or NL
		or EOI followed by NL. If the data stream is not concluded with either EOI or NL, the R&S NGU will wait for additional
		data. In the case of a binary data transmission, the R&S NGU ignores the bit combination NL (0Ah) within the data stream.
		The binary data block has the following structure: #<LengthofLength><Length><block_data>
			INTRO_CMD_HELP: Example: #234<block_data> \n
			- <LengthofLength> specifies how many positions the subsequent length specification occupies ('2' in the example)
			- <Length> specifies the number of subsequent bytes ('34' in the example)
			- <binary block data> specifies the binary block data of the specified length
		To configure fastlog for scpi target, see Example 'Configuring fastlog for scpi target'. \n
			:return: result: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('FLOG:DATA?')
		return response

	def get_triggered(self) -> bool:
		"""SCPI: FLOG:TRIGgered \n
		Snippet: value: bool = driver.flog.get_triggered() \n
		Sets or queries the triggered state of FastLog. See Figure 'Overview of trigger IO system'. \n
			:return: arg_0: 1 Activates the FastLog state. 0 Deactivates the FastLog state.
		"""
		response = self._core.io.query_str('FLOG:TRIGgered?')
		return Conversions.str_to_bool(response)

	def set_triggered(self, arg_0: bool) -> None:
		"""SCPI: FLOG:TRIGgered \n
		Snippet: driver.flog.set_triggered(arg_0 = False) \n
		Sets or queries the triggered state of FastLog. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: 1 Activates the FastLog state. 0 Deactivates the FastLog state.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'FLOG:TRIGgered {param}')

	# noinspection PyTypeChecker
	def get_symbol_rate(self) -> enums.FastLogSampleRate:
		"""SCPI: FLOG:SRATe \n
		Snippet: value: enums.FastLogSampleRate = driver.flog.get_symbol_rate() \n
		Sets or queries the sample rate of the FastLog function. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('FLOG:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.FastLogSampleRate)

	def set_symbol_rate(self, arg_0: enums.FastLogSampleRate) -> None:
		"""SCPI: FLOG:SRATe \n
		Snippet: driver.flog.set_symbol_rate(arg_0 = enums.FastLogSampleRate.S001k) \n
		Sets or queries the sample rate of the FastLog function. \n
			:param arg_0: 500K | 250K | 125K | 62K5 | 31K25 | 15K625 | 7K812 | 3K906 | 1K953 | 976 | 488 | 244 | 122 | 61 | 30 | 15
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.FastLogSampleRate)
		self._core.io.write(f'FLOG:SRATe {param}')

	def get_stime(self) -> float:
		"""SCPI: FLOG:STIMe \n
		Snippet: value: float = driver.flog.get_stime() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('FLOG:STIMe?')
		return Conversions.str_to_float(response)

	def set_stime(self, arg_0: float) -> None:
		"""SCPI: FLOG:STIMe \n
		Snippet: driver.flog.set_stime(arg_0 = 1.0) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'FLOG:STIMe {param}')

	# noinspection PyTypeChecker
	def get_target(self) -> enums.FastLogTarget:
		"""SCPI: FLOG:TARGet \n
		Snippet: value: enums.FastLogTarget = driver.flog.get_target() \n
		Chose the target the data shall be written to. \n
			:return: arg_0: SCPI | USB SCPI Transfer data to SCPI client. The sum of all sample rates have to be smaller or equal to 500 kS/s. USB Saves data to a binary file which is saved to the direectory specified in the 'Target Folder'.
		"""
		response = self._core.io.query_str('FLOG:TARGet?')
		return Conversions.str_to_scalar_enum(response, enums.FastLogTarget)

	def set_target(self, arg_0: enums.FastLogTarget) -> None:
		"""SCPI: FLOG:TARGet \n
		Snippet: driver.flog.set_target(arg_0 = enums.FastLogTarget.SCPI) \n
		Chose the target the data shall be written to. \n
			:param arg_0: SCPI | USB SCPI Transfer data to SCPI client. The sum of all sample rates have to be smaller or equal to 500 kS/s. USB Saves data to a binary file which is saved to the direectory specified in the 'Target Folder'.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.FastLogTarget)
		self._core.io.write(f'FLOG:TARGet {param}')
