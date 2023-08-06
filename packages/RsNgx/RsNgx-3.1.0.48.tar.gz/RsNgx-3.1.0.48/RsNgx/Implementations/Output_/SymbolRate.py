from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def get_state(self) -> bool:
		"""SCPI: OUTPut:SRATe[:STATe] \n
		Snippet: value: bool = driver.output.symbolRate.get_state() \n
		Sets or queries the reduce slew rate option for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:SRATe:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:SRATe[:STATe] \n
		Snippet: driver.output.symbolRate.set_state(arg_0 = False) \n
		Sets or queries the reduce slew rate option for the selected channel. \n
			:param arg_0:
				- 1: Activates reduce slew rate option for the selected channel.
				- 0: Deactivates reduce slew rate option for the selected channel."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:SRATe:STATe {param}')
