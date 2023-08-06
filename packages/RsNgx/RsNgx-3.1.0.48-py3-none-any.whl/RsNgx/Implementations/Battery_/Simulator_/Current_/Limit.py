from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	def get_eod(self) -> float:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:EOD \n
		Snippet: value: float = driver.battery.simulator.current.limit.get_eod() \n
		Sets or queries the current limit at end-of-discharge. \n
			:return: arg_0: Sets the current limit at end-of-discharge.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CURRent:LIMit:EOD?')
		return Conversions.str_to_float(response)

	def set_eod(self, arg_0: float) -> None:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:EOD \n
		Snippet: driver.battery.simulator.current.limit.set_eod(arg_0 = 1.0) \n
		Sets or queries the current limit at end-of-discharge. \n
			:param arg_0: Sets the current limit at end-of-discharge.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:CURRent:LIMit:EOD {param}')

	def get_regular(self) -> float:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:REGular \n
		Snippet: value: float = driver.battery.simulator.current.limit.get_regular() \n
		Sets or queries the current limit at regular charge level. \n
			:return: arg_0: Sets the current limit at regular charge level.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CURRent:LIMit:REGular?')
		return Conversions.str_to_float(response)

	def set_regular(self, arg_0: float) -> None:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:REGular \n
		Snippet: driver.battery.simulator.current.limit.set_regular(arg_0 = 1.0) \n
		Sets or queries the current limit at regular charge level. \n
			:param arg_0: Sets the current limit at regular charge level.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:CURRent:LIMit:REGular {param}')

	def get_eoc(self) -> float:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:EOC \n
		Snippet: value: float = driver.battery.simulator.current.limit.get_eoc() \n
		Sets or queries the current limit at end-of-charge. \n
			:return: arg_0: Sets the current limit at end-of-charge.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CURRent:LIMit:EOC?')
		return Conversions.str_to_float(response)

	def set_eoc(self, arg_0: float) -> None:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit:EOC \n
		Snippet: driver.battery.simulator.current.limit.set_eoc(arg_0 = 1.0) \n
		Sets or queries the current limit at end-of-charge. \n
			:param arg_0: Sets the current limit at end-of-charge.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:CURRent:LIMit:EOC {param}')

	def get_value(self) -> float:
		"""SCPI: BATTery:SIMulator:CURRent:LIMit \n
		Snippet: value: float = driver.battery.simulator.current.limit.get_value() \n
		Sets or queries the current limit from specific channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CURRent:LIMit?')
		return Conversions.str_to_float(response)
