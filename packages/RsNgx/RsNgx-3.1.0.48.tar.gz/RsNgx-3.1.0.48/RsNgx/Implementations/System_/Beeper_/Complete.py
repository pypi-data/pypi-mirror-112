from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Complete:
	"""Complete commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("complete", core, parent)

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Complete_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate

	def get_state(self) -> bool:
		"""SCPI: SYSTem:BEEPer[:COMPlete]:STATe \n
		Snippet: value: bool = driver.system.beeper.complete.get_state() \n
		Sets or queries the beeper tone. \n
			:return: beeper_state: No help available
		"""
		response = self._core.io.query_str('SYSTem:BEEPer:COMPlete:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, beeper_state: bool) -> None:
		"""SCPI: SYSTem:BEEPer[:COMPlete]:STATe \n
		Snippet: driver.system.beeper.complete.set_state(beeper_state = False) \n
		Sets or queries the beeper tone. \n
			:param beeper_state: 1 | 0 ON OFF - Control beeper is deactivated. OFF ON - Control beeper is activated.
		"""
		param = Conversions.bool_to_str(beeper_state)
		self._core.io.write(f'SYSTem:BEEPer:COMPlete:STATe {param}')
