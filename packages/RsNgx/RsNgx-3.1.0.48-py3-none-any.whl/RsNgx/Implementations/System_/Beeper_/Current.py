from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SYSTem:BEEPer:CURRent:STATe \n
		Snippet: value: bool = driver.system.beeper.current.get_state() \n
		Sets or queries current control beeper tone state. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SYSTem:BEEPer:CURRent:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: SYSTem:BEEPer:CURRent:STATe \n
		Snippet: driver.system.beeper.current.set_state(arg_0 = False) \n
		Sets or queries current control beeper tone state. \n
			:param arg_0:
				- 1: Control beeper is activated.
				- 0: Control beeper is deactivated."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SYSTem:BEEPer:CURRent:STATe {param}')
