from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Resistance:
	"""Resistance commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("resistance", core, parent)

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Resistance_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:RESistance:STATe \n
		Snippet: value: bool = driver.source.resistance.get_state() \n
		Sets or queries the constant resistance mode. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:RESistance:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: [SOURce]:RESistance:STATe \n
		Snippet: driver.source.resistance.set_state(arg_0 = False) \n
		Sets or queries the constant resistance mode. \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SOURce:RESistance:STATe {param}')
