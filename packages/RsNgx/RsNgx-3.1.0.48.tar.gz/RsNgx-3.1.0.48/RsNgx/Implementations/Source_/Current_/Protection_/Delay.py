from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def get_initial(self) -> float:
		"""SCPI: [SOURce]:CURRent:PROTection:DELay:INITial \n
		Snippet: value: float = driver.source.current.protection.delay.get_initial() \n
		Sets or queries the initial fuse delay time once output turns on. \n
			:return: voltage: No help available
		"""
		response = self._core.io.query_str('SOURce:CURRent:PROTection:DELay:INITial?')
		return Conversions.str_to_float(response)

	def set_initial(self, voltage: float) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:DELay:INITial \n
		Snippet: driver.source.current.protection.delay.set_initial(voltage = 1.0) \n
		Sets or queries the initial fuse delay time once output turns on. \n
			:param voltage: No help available
		"""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:CURRent:PROTection:DELay:INITial {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce]:CURRent:PROTection:DELay \n
		Snippet: value: float = driver.source.current.protection.delay.get_value() \n
		Sets or queries the fuse delay time. \n
			:return: voltage: No help available
		"""
		response = self._core.io.query_str('SOURce:CURRent:PROTection:DELay?')
		return Conversions.str_to_float(response)

	def set_value(self, voltage: float) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:DELay \n
		Snippet: driver.source.current.protection.delay.set_value(voltage = 1.0) \n
		Sets or queries the fuse delay time. \n
			:param voltage: No help available
		"""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:CURRent:PROTection:DELay {param}')
