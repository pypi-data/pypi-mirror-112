from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def get_state(self) -> bool:
		"""SCPI: OUTPut:DELay[:STATe] \n
		Snippet: value: bool = driver.output.delay.get_state() \n
		Sets or queries the output delay state for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:DELay:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:DELay[:STATe] \n
		Snippet: driver.output.delay.set_state(arg_0 = False) \n
		Sets or queries the output delay state for the selected channel. \n
			:param arg_0:
				- 0: Deactivates output delay for the selected channel.
				- 1: Activates output delay for the selected channel."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:DELay:STATe {param}')

	def get_duration(self) -> float:
		"""SCPI: OUTPut:DELay:DURation \n
		Snippet: value: float = driver.output.delay.get_duration() \n
		Sets or queries the duration for output delay. \n
			:return: sequence_delay: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:DELay:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, sequence_delay: float) -> None:
		"""SCPI: OUTPut:DELay:DURation \n
		Snippet: driver.output.delay.set_duration(sequence_delay = 1.0) \n
		Sets or queries the duration for output delay. \n
			:param sequence_delay:
				- numeric value: Numeric value of the duration in seconds.
				- MIN | MINimum: Minimum value of the duration at 0.001 seconds.
				- MAX | MAXimum: Maximum value of the duration at 10.00 seconds."""
		param = Conversions.decimal_value_to_str(sequence_delay)
		self._core.io.write_with_opc(f'OUTPut:DELay:DURation {param}')
