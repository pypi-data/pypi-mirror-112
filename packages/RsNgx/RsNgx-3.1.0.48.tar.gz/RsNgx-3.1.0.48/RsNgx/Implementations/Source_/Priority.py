from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Priority:
	"""Priority commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("priority", core, parent)

	def set(self, arg_0: str) -> None:
		"""SCPI: SOURce:PRIority \n
		Snippet: driver.source.priority.set(arg_0 = r1) \n
		Sets or queries the source priority mode. \n
			:param arg_0: VOLTage | CURRent | list VOLT Set the source measure unit to operate in voltage priority mode. CURR Set the source measure unit to operate in current priority mode.
		"""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write(f'SOURce:PRIority {param}')

	def get(self, arg_0: str, channel_list: str = None) -> str:
		"""SCPI: SOURce:PRIority \n
		Snippet: value: str = driver.source.priority.get(arg_0 = r1, channel_list = r1) \n
		Sets or queries the source priority mode. \n
			:param arg_0: VOLTage | CURRent | list VOLT Set the source measure unit to operate in voltage priority mode. CURR Set the source measure unit to operate in current priority mode.
			:param channel_list: list
			:return: arg_0: VOLTage | CURRent | list VOLT Set the source measure unit to operate in voltage priority mode. CURR Set the source measure unit to operate in current priority mode."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.RawString), ArgSingle('channel_list', channel_list, DataType.RawString, True))
		response = self._core.io.query_str(f'SOURce:PRIority? {param}'.rstrip())
		return trim_str_response(response)
