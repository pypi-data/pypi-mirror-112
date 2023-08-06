from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fault:
	"""Fault commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fault", core, parent)

	def get_state(self) -> bool:
		"""SCPI: DIO:FAULt[:STATe] \n
		Snippet: value: bool = driver.dio.fault.get_state() \n
		Sets or queries the digital output fault. See 'operation modes' in Figure 'Overview of trigger IO system' \n
			:return: arg_0: 1 Enables digital output fault. 0 Disables digital output fault.
		"""
		response = self._core.io.query_str('DIO:FAULt:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: DIO:FAULt[:STATe] \n
		Snippet: driver.dio.fault.set_state(arg_0 = False) \n
		Sets or queries the digital output fault. See 'operation modes' in Figure 'Overview of trigger IO system' \n
			:param arg_0: 1 Enables digital output fault. 0 Disables digital output fault.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'DIO:FAULt:STATe {param}')

	def get_channel(self) -> int:
		"""SCPI: DIO:FAULt:CHANnel \n
		Snippet: value: int = driver.dio.fault.get_channel() \n
		Sets or queries channel selection for the digital output fault source. See 'operation modes' in Figure 'Overview of
		trigger IO system'. \n
			:return: arg_0: 1 | 2
		"""
		response = self._core.io.query_str('DIO:FAULt:CHANnel?')
		return Conversions.str_to_int(response)

	def set_channel(self, arg_0: int) -> None:
		"""SCPI: DIO:FAULt:CHANnel \n
		Snippet: driver.dio.fault.set_channel(arg_0 = 1) \n
		Sets or queries channel selection for the digital output fault source. See 'operation modes' in Figure 'Overview of
		trigger IO system'. \n
			:param arg_0: 1 | 2
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'DIO:FAULt:CHANnel {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.DioFaultSource:
		"""SCPI: DIO:FAULt:SOURce \n
		Snippet: value: enums.DioFaultSource = driver.dio.fault.get_source() \n
		Sets or queries the 'operation modes' of the digital output fault source See 'operation modes' in Figure 'Overview of
		trigger IO system'. \n
			:return: arg_0: CC | CV | CR | SINK | PROTection | OUTPut If 'OUTPut' is selected, the 'fault output' will be active if the output of the selected channel is off.
		"""
		response = self._core.io.query_str('DIO:FAULt:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.DioFaultSource)

	def set_source(self, arg_0: enums.DioFaultSource) -> None:
		"""SCPI: DIO:FAULt:SOURce \n
		Snippet: driver.dio.fault.set_source(arg_0 = enums.DioFaultSource.CC) \n
		Sets or queries the 'operation modes' of the digital output fault source See 'operation modes' in Figure 'Overview of
		trigger IO system'. \n
			:param arg_0: CC | CV | CR | SINK | PROTection | OUTPut If 'OUTPut' is selected, the 'fault output' will be active if the output of the selected channel is off.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.DioFaultSource)
		self._core.io.write(f'DIO:FAULt:SOURce {param}')

	# noinspection PyTypeChecker
	def get_signal(self) -> enums.DioSignal:
		"""SCPI: DIO:FAULt:SIGNal \n
		Snippet: value: enums.DioSignal = driver.dio.fault.get_signal() \n
		Select digital output fault signal type. \n
			:return: arg_0: CONStant | PULSe CONStant An constant level trigger signal is sent out PULSe An output pulse of 100 ms trigger signal is sent out
		"""
		response = self._core.io.query_str('DIO:FAULt:SIGNal?')
		return Conversions.str_to_scalar_enum(response, enums.DioSignal)

	def set_signal(self, arg_0: enums.DioSignal) -> None:
		"""SCPI: DIO:FAULt:SIGNal \n
		Snippet: driver.dio.fault.set_signal(arg_0 = enums.DioSignal.CONStant) \n
		Select digital output fault signal type. \n
			:param arg_0: CONStant | PULSe CONStant An constant level trigger signal is sent out PULSe An output pulse of 100 ms trigger signal is sent out
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.DioSignal)
		self._core.io.write(f'DIO:FAULt:SIGNal {param}')
