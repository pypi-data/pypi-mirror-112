from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alimit:
	"""Alimit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alimit", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:ALIMit[:STATe] \n
		Snippet: value: bool = driver.source.alimit.get_state() \n
		Sets or queries the safety limit state. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:ALIMit:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: [SOURce]:ALIMit[:STATe] \n
		Snippet: driver.source.alimit.set_state(arg_0 = False) \n
		Sets or queries the safety limit state. \n
			:param arg_0:
				- 1: Activates the safety limit.
				- 0: Deactivates the safety limit."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SOURce:ALIMit:STATe {param}')
