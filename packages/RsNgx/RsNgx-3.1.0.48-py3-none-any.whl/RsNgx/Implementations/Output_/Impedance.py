from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Impedance:
	"""Impedance commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("impedance", core, parent)

	def get_state(self) -> bool:
		"""SCPI: OUTPut:IMPedance[:STATe] \n
		Snippet: value: bool = driver.output.impedance.get_state() \n
		Sets or queries the impedance target for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:IMPedance:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:IMPedance[:STATe] \n
		Snippet: driver.output.impedance.set_state(arg_0 = False) \n
		Sets or queries the impedance target for the selected channel. \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:IMPedance:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: OUTPut:IMPedance \n
		Snippet: value: float = driver.output.impedance.get_value() \n
		Sets or queries source impedance for the signal specified in ohms. \n
			:return: arg_0: numeric value | MIN | MINimum | MAX | MAXimum | DEF | DEFault | list numeric value Numeric value of the impedance ohm. MIN | MINimum Minimum value of the impedance at -0.05 ohms. MAX | MAXimum Maximum value of the impedance at 100 ohms. DEF Default value of the impedance at 0 ohms. Unit: ohm
		"""
		response = self._core.io.query_str_with_opc('OUTPut:IMPedance?')
		return Conversions.str_to_float(response)

	def set_value(self, arg_0: float) -> None:
		"""SCPI: OUTPut:IMPedance \n
		Snippet: driver.output.impedance.set_value(arg_0 = 1.0) \n
		Sets or queries source impedance for the signal specified in ohms. \n
			:param arg_0: numeric value | MIN | MINimum | MAX | MAXimum | DEF | DEFault | list numeric value Numeric value of the impedance ohm. MIN | MINimum Minimum value of the impedance at -0.05 ohms. MAX | MAXimum Maximum value of the impedance at 100 ohms. DEF Default value of the impedance at 0 ohms. Unit: ohm
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:IMPedance {param}')
