from typing import List

from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fuse:
	"""Fuse commands group definition. 6 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fuse", core, parent)

	@property
	def link(self):
		"""link commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_link'):
			from .Fuse_.Link import Link
			self._link = Link(self._core, self._base)
		return self._link

	@property
	def tripped(self):
		"""tripped commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tripped'):
			from .Fuse_.Tripped import Tripped
			self._tripped = Tripped(self._core, self._base)
		return self._tripped

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Fuse_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	def get_state(self) -> bool:
		"""SCPI: FUSE[:STATe] \n
		Snippet: value: bool = driver.fuse.get_state() \n
		Sets or queries the state for over current protection (OCP) . See Example 'Configuring fuses'. \n
			:return: arg_0:
				- 1 | 0:
				- 1: Activates the OCP state.
				- 0: deactivates the OCP state."""
		response = self._core.io.query_str('FUSE:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: FUSE[:STATe] \n
		Snippet: driver.fuse.set_state(arg_0 = False) \n
		Sets or queries the state for over current protection (OCP) . See Example 'Configuring fuses'. \n
			:param arg_0:
				- 1 | 0:
				- 1: Activates the OCP state.
				- 0: deactivates the OCP state."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'FUSE:STATe {param}')

	def set_unlink(self, arg_0: List[int]) -> None:
		"""SCPI: FUSE:UNLink \n
		Snippet: driver.fuse.set_unlink(arg_0 = [1, 2, 3]) \n
		Unlinks fuse linking from the other channels (Ch 1, Ch 2, Ch 3 or Ch 4) . See Example 'Configuring fuses'. \n
			:param arg_0: 0 - Unlink all other channels to the previously selected channel.
		"""
		param = Conversions.list_to_csv_str(arg_0)
		self._core.io.write(f'FUSE:UNLink {param}')
