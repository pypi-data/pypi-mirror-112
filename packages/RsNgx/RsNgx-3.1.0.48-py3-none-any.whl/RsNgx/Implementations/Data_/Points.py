from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Points:
	"""Points commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("points", core, parent)

	def get(self, arg_0: str) -> int:
		"""SCPI: DATA:POINts \n
		Snippet: value: int = driver.data.points.get(arg_0 = '1') \n
		Queries the number of measurements from the selected logging file. If manual trigger mode (trigger via TRIG function) is
		used, the logging function has to be activated. Without activating the logging function in the manual trigger mode, the
		instrument is not able to save a logging file internally or on the USB stick. \n
			:param arg_0: Filepath of the logging file data.
			:return: result: No help available"""
		param = Conversions.value_to_quoted_str(arg_0)
		response = self._core.io.query_str(f'DATA:POINts? {param}')
		return Conversions.str_to_int(response)
