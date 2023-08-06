from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SYSTem:BEEPer:OUTPut:STATe \n
		Snippet: value: bool = driver.system.beeper.output.get_state() \n
		Sets or queries output beeper tone state. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('SYSTem:BEEPer:OUTPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:BEEPer:OUTPut:STATe \n
		Snippet: driver.system.beeper.output.set_state(arg_0 = False) \n
		Sets or queries output beeper tone state. \n
			:param arg_0:
				- 1: Output beeper is activated.
				- 0: Output beeper is deactivated."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'SYSTem:BEEPer:OUTPut:STATe {param}')
