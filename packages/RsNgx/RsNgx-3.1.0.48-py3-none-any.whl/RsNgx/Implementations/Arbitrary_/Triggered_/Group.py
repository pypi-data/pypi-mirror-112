from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Group:
	"""Group commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("group", core, parent)

	def get_state(self) -> int or bool:
		"""SCPI: ARBitrary:TRIGgered:GROup[:STATe] \n
		Snippet: value: int or bool = driver.arbitrary.triggered.group.get_state() \n
		Sets or queries the trigger condition of the arbitrary step group for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:TRIGgered:GROup:STATe?')
		return Conversions.str_to_int_or_bool(response)

	def set_state(self, arg_0: int or bool) -> None:
		"""SCPI: ARBitrary:TRIGgered:GROup[:STATe] \n
		Snippet: driver.arbitrary.triggered.group.set_state(arg_0 = 1) \n
		Sets or queries the trigger condition of the arbitrary step group for the selected channel. \n
			:param arg_0:
				- OFF: There is no DIO pin that has a mode set to arbitrary step group for the selected channel.
				- 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8: DIO pin/s are enabled with a mode set to arbitrary step group for the selected channel.When DIO pin is enabled with arbitrary step point mode, QuickArb function will step to the next point when the correct voltage is applied to the DIO pin."""
		param = Conversions.decimal_or_bool_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:TRIGgered:GROup:STATe {param}')
