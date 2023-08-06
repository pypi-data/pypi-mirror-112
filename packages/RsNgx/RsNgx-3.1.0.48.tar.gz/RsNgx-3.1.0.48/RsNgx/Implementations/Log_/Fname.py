from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fname:
	"""Fname commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fname", core, parent)

	def set(self, set_new_value: str) -> None:
		"""SCPI: LOG:FNAMe \n
		Snippet: driver.log.fname.set(set_new_value = '1') \n
		Sets or queries the filename and storage location for the data logging. \n
			:param set_new_value: No help available
		"""
		param = Conversions.value_to_quoted_str(set_new_value)
		self._core.io.write(f'LOG:FNAMe {param}')

	def get(self) -> str:
		"""SCPI: LOG:FNAMe \n
		Snippet: value: str = driver.log.fname.get() \n
		Sets or queries the filename and storage location for the data logging. \n
			:return: set_new_value: No help available"""
		response = self._core.io.query_str(f'LOG:FNAMe?')
		return trim_str_response(response)
