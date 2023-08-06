from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)

	def get_state(self) -> bool:
		"""SCPI: LOG:CHANnel[:STATe] \n
		Snippet: value: bool = driver.log.channel.get_state() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('LOG:CHANnel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: LOG:CHANnel[:STATe] \n
		Snippet: driver.log.channel.set_state(arg_0 = False) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'LOG:CHANnel:STATe {param}')
