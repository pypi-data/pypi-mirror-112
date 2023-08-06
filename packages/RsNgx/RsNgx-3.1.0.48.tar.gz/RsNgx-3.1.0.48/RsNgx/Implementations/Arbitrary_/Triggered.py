from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Triggered:
	"""Triggered commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("triggered", core, parent)

	@property
	def point(self):
		"""point commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_point'):
			from .Triggered_.Point import Point
			self._point = Point(self._core, self._base)
		return self._point

	@property
	def group(self):
		"""group commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_group'):
			from .Triggered_.Group import Group
			self._group = Group(self._core, self._base)
		return self._group

	def get_state(self) -> int or bool:
		"""SCPI: ARBitrary:TRIGgered[:STATe] \n
		Snippet: value: int or bool = driver.arbitrary.triggered.get_state() \n
		Sets or queries the trigger condition of the arbitrary for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:TRIGgered:STATe?')
		return Conversions.str_to_int_or_bool(response)

	def set_state(self, arg_0: int or bool) -> None:
		"""SCPI: ARBitrary:TRIGgered[:STATe] \n
		Snippet: driver.arbitrary.triggered.set_state(arg_0 = 1) \n
		Sets or queries the trigger condition of the arbitrary for the selected channel. \n
			:param arg_0:
				- OFF: There is no DIO pin that has a mode set to arbitrary for the selected channel.
				- 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8: DIO pin/s are enabled with a mode set to arbitrary for the selected channel.When DIO pin is enabled with arbitrary mode, QuickArb function of the channel assigned to that pin will be enabled when the correct voltage is applied to the DIO pin."""
		param = Conversions.decimal_or_bool_value_to_str(arg_0)
		self._core.io.write(f'ARBitrary:TRIGgered:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbTrigMode:
		"""SCPI: ARBitrary:TRIGgered:MODE \n
		Snippet: value: enums.ArbTrigMode = driver.arbitrary.triggered.get_mode() \n
		Sets or queries the arbitrary trigger mode of the previous selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:TRIGgered:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbTrigMode)

	def set_mode(self, arg_0: enums.ArbTrigMode) -> None:
		"""SCPI: ARBitrary:TRIGgered:MODE \n
		Snippet: driver.arbitrary.triggered.set_mode(arg_0 = enums.ArbTrigMode.RUN) \n
		Sets or queries the arbitrary trigger mode of the previous selected channel. \n
			:param arg_0: SINGle | RUN SINGle A trigger event starts only with one arbitrary sequence. RUN A trigger event starts the whole arbitrary sequences (with all repetitions) .
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.ArbTrigMode)
		self._core.io.write(f'ARBitrary:TRIGgered:MODE {param}')
