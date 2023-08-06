from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	def set(self, arg_0: int, arg_1: enums.DioSignal) -> None:
		"""SCPI: DIO:OUTPut:SIGNal \n
		Snippet: driver.dio.output.signal.set(arg_0 = 1, arg_1 = enums.DioSignal.CONStant) \n
		Select digital output signal type. \n
			:param arg_0: Channel number.
			:param arg_1: CONStant | PULSe CONStant An constant level trigger signal is sent out PULSe An output pulse of 100 ms trigger signal is sent out
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Integer), ArgSingle('arg_1', arg_1, DataType.Enum))
		self._core.io.write_with_opc(f'DIO:OUTPut:SIGNal {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, arg_0: int) -> enums.DioSignal:
		"""SCPI: DIO:OUTPut:SIGNal \n
		Snippet: value: enums.DioSignal = driver.dio.output.signal.get(arg_0 = 1) \n
		Select digital output signal type. \n
			:param arg_0: Channel number.
			:return: arg_1: CONStant | PULSe CONStant An constant level trigger signal is sent out PULSe An output pulse of 100 ms trigger signal is sent out"""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str_with_opc(f'DIO:OUTPut:SIGNal? {param}')
		return Conversions.str_to_scalar_enum(response, enums.DioSignal)
