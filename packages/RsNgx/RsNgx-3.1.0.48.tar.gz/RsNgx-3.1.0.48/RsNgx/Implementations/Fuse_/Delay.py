from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def get_initial(self) -> float:
		"""SCPI: FUSE:DELay:INITial \n
		Snippet: value: float = driver.fuse.delay.get_initial() \n
		Sets the initial fuse delay time once output turns on. \n
			:return: voltage: No help available
		"""
		response = self._core.io.query_str('FUSE:DELay:INITial?')
		return Conversions.str_to_float(response)

	def set_initial(self, voltage: float) -> None:
		"""SCPI: FUSE:DELay:INITial \n
		Snippet: driver.fuse.delay.set_initial(voltage = 1.0) \n
		Sets the initial fuse delay time once output turns on. \n
			:param voltage:
				- numeric value: Numeric value for initial fuse delay.
				- MIN | MINimum: Min value for initial fuse delay.
				- MAX | MAXimum: Max value for initial fuse delay."""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'FUSE:DELay:INITial {param}')
