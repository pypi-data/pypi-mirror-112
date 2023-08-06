from typing import List

from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def points(self):
		"""points commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_points'):
			from .Data_.Points import Points
			self._points = Points(self._core, self._base)
		return self._points

	def delete(self, arg_0: str) -> None:
		"""SCPI: DATA:DELete \n
		Snippet: driver.data.delete(arg_0 = '1') \n
		Deletes the specified file from memory. \n
			:param arg_0: Filepath of the file.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'DATA:DELete {param}')

	def get_list_py(self) -> List[str]:
		"""SCPI: DATA:LIST \n
		Snippet: value: List[str] = driver.data.get_list_py() \n
		Queries all files in internal memory ('/int/') and external memory ('/USB') . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('DATA:LIST?')
		return Conversions.str_to_str_list(response)
