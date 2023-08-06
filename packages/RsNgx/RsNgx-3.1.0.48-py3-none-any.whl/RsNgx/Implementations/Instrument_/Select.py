from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, channel: int) -> None:
		"""SCPI: INSTrument:NSELect \n
		Snippet: driver.instrument.select.set(channel = 1) \n
		Selects or queries the channel by number. \n
			:param channel: No help available
		"""
		param = Conversions.decimal_value_to_str(channel)
		self._core.io.write(f'INSTrument:NSELect {param}')

	def get(self) -> int:
		"""SCPI: INSTrument:NSELect \n
		Snippet: value: int = driver.instrument.select.get() \n
		Selects or queries the channel by number. \n
			:return: channel: No help available"""
		response = self._core.io.query_str(f'INSTrument:NSELect?')
		return Conversions.str_to_int(response)
