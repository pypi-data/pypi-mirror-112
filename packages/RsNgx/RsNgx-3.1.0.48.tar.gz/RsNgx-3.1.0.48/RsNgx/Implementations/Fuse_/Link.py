from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Link:
	"""Link commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("link", core, parent)

	def set(self, arg_0: List[int]) -> None:
		"""SCPI: FUSE:LINK \n
		Snippet: driver.fuse.link.set(arg_0 = [1, 2, 3]) \n
		Sets or queries the fuses of several selected channels (fuse linking) . \n
			:param arg_0: 0 - Link all other channels to the previously selected channel.
		"""
		param = Conversions.list_to_csv_str(arg_0)
		self._core.io.write(f'FUSE:LINK {param}')

	def get(self, arg_0: List[int]) -> List[int]:
		"""SCPI: FUSE:LINK \n
		Snippet: value: List[int] = driver.fuse.link.get(arg_0 = [1, 2, 3]) \n
		Sets or queries the fuses of several selected channels (fuse linking) . \n
			:param arg_0: 0 - Link all other channels to the previously selected channel.
			:return: arg_0: 0 - Link all other channels to the previously selected channel."""
		param = Conversions.list_to_csv_str(arg_0)
		response = self._core.io.query_bin_or_ascii_int_list(f'FUSE:LINK? {param}')
		return response
