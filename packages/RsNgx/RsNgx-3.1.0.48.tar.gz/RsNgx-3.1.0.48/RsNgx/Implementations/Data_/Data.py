from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def get(self, arg_0: str) -> str:
		"""SCPI: DATA:DATA \n
		Snippet: value: str = driver.data.data.get(arg_0 = '1') \n
		Returns the logging file data of the selected file. If manual trigger mode (trigger via TRIG function) is used, the
		logging function has to be activated. Without activating the logging function in the manual trigger mode, the instrument
		is not able to save a logging file internally or on the USB stick. \n
			:param arg_0: Filepath of the logging file data.
			:return: result: No help available"""
		param = Conversions.value_to_quoted_str(arg_0)
		response = self._core.io.query_str(f'DATA:DATA? {param}')
		return trim_str_response(response)
