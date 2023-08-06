from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	def get_eod(self) -> float:
		"""SCPI: BATTery:MODel:CURRent:LIMit:EOD \n
		Snippet: value: float = driver.battery.model.current.limit.get_eod() \n
		Sets or queries the current limit of the battery model at end-of-discharge. \n
			:return: arg_0: Sets the current limit of the battery model at end-of-discharge.
		"""
		response = self._core.io.query_str('BATTery:MODel:CURRent:LIMit:EOD?')
		return Conversions.str_to_float(response)

	def set_eod(self, arg_0: float) -> None:
		"""SCPI: BATTery:MODel:CURRent:LIMit:EOD \n
		Snippet: driver.battery.model.current.limit.set_eod(arg_0 = 1.0) \n
		Sets or queries the current limit of the battery model at end-of-discharge. \n
			:param arg_0: Sets the current limit of the battery model at end-of-discharge.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:CURRent:LIMit:EOD {param}')

	def get_regular(self) -> float:
		"""SCPI: BATTery:MODel:CURRent:LIMit:REGular \n
		Snippet: value: float = driver.battery.model.current.limit.get_regular() \n
		Sets or queries the current limit of the battery model at regular charge level. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('BATTery:MODel:CURRent:LIMit:REGular?')
		return Conversions.str_to_float(response)

	def set_regular(self, arg_0: float) -> None:
		"""SCPI: BATTery:MODel:CURRent:LIMit:REGular \n
		Snippet: driver.battery.model.current.limit.set_regular(arg_0 = 1.0) \n
		Sets or queries the current limit of the battery model at regular charge level. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:CURRent:LIMit:REGular {param}')

	def get_eoc(self) -> float:
		"""SCPI: BATTery:MODel:CURRent:LIMit:EOC \n
		Snippet: value: float = driver.battery.model.current.limit.get_eoc() \n
		Sets or queries the current limit of the battery model at end-of-charge. \n
			:return: arg_0: Sets the current limit of the battery model at end-of-charge.
		"""
		response = self._core.io.query_str('BATTery:MODel:CURRent:LIMit:EOC?')
		return Conversions.str_to_float(response)

	def set_eoc(self, arg_0: float) -> None:
		"""SCPI: BATTery:MODel:CURRent:LIMit:EOC \n
		Snippet: driver.battery.model.current.limit.set_eoc(arg_0 = 1.0) \n
		Sets or queries the current limit of the battery model at end-of-charge. \n
			:param arg_0: Sets the current limit of the battery model at end-of-charge.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:MODel:CURRent:LIMit:EOC {param}')
