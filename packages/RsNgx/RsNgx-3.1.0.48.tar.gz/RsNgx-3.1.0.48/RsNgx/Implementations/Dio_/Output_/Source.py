from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def set(self, arg_0: int, arg_1: enums.DioOutSource) -> None:
		"""SCPI: DIO:OUTPut:SOURce \n
		Snippet: driver.dio.output.source.set(arg_0 = 1, arg_1 = enums.DioOutSource.FORCed) \n
		Sets or queries the digital output source. See 'operation modes' in Figure 'Overview of trigger IO system'. \n
			:param arg_0: 1 Channel selection for the digital output source.
			:param arg_1: OUTPut | TRIGger | FORCed OUTPut Selected channel output is used as the digital output source. TRIGger Selected channel external trigger signal is used as the digital output source. FORCed Selected output is forced to high level and can be switched by method RsNgx.Dio.Output.State.set command.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Integer), ArgSingle('arg_1', arg_1, DataType.Enum))
		self._core.io.write_with_opc(f'DIO:OUTPut:SOURce {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, arg_0: int) -> enums.DioOutSource:
		"""SCPI: DIO:OUTPut:SOURce \n
		Snippet: value: enums.DioOutSource = driver.dio.output.source.get(arg_0 = 1) \n
		Sets or queries the digital output source. See 'operation modes' in Figure 'Overview of trigger IO system'. \n
			:param arg_0: 1 Channel selection for the digital output source.
			:return: arg_1: OUTPut | TRIGger | FORCed OUTPut Selected channel output is used as the digital output source. TRIGger Selected channel external trigger signal is used as the digital output source. FORCed Selected output is forced to high level and can be switched by method RsNgx.Dio.Output.State.set command."""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str_with_opc(f'DIO:OUTPut:SOURce? {param}')
		return Conversions.str_to_scalar_enum(response, enums.DioOutSource)
