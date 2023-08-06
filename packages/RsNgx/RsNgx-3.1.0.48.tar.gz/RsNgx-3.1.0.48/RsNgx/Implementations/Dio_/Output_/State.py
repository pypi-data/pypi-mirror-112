from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, arg_0: int, arg_1: bool) -> None:
		"""SCPI: DIO:OUTPut[:STATe] \n
		Snippet: driver.dio.output.state.set(arg_0 = 1, arg_1 = False) \n
		Sets or queries the digital output channel selection. \n
			:param arg_0: 1 Channel selection for the digital output source.
			:param arg_1: 1 | 0 Enables or disables the digital output state.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Integer), ArgSingle('arg_1', arg_1, DataType.Boolean))
		self._core.io.write_with_opc(f'DIO:OUTPut:STATe {param}'.rstrip())

	def get(self, arg_0: int) -> bool:
		"""SCPI: DIO:OUTPut[:STATe] \n
		Snippet: value: bool = driver.dio.output.state.get(arg_0 = 1) \n
		Sets or queries the digital output channel selection. \n
			:param arg_0: 1 Channel selection for the digital output source.
			:return: arg_1: 1 | 0 Enables or disables the digital output state."""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str_with_opc(f'DIO:OUTPut:STATe? {param}')
		return Conversions.str_to_bool(response)
