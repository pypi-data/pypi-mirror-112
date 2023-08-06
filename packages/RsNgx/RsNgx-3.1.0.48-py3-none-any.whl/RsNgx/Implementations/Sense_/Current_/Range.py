from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("range", core, parent)

	def get_upper(self) -> float:
		"""SCPI: SENSe:CURRent:RANGe[:UPPer] \n
		Snippet: value: float = driver.sense.current.range.get_upper() \n
		Sets or queries the current range for measurement. There is a selection of 10 A, 1 A, 100 mA and 10 mA range. \n
			:return: arg_0: Defines the current range for measurement (10 A, 1 A, 100 mA and 10 mA) . Unit: A
		"""
		response = self._core.io.query_str('SENSe:CURRent:RANGe:UPPer?')
		return Conversions.str_to_float(response)

	def set_upper(self, arg_0: float) -> None:
		"""SCPI: SENSe:CURRent:RANGe[:UPPer] \n
		Snippet: driver.sense.current.range.set_upper(arg_0 = 1.0) \n
		Sets or queries the current range for measurement. There is a selection of 10 A, 1 A, 100 mA and 10 mA range. \n
			:param arg_0: Defines the current range for measurement (10 A, 1 A, 100 mA and 10 mA) . Unit: A
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SENSe:CURRent:RANGe:UPPer {param}')

	def get_lower(self) -> float:
		"""SCPI: SENSe:CURRent:RANGe:LOWer \n
		Snippet: value: float = driver.sense.current.range.get_lower() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SENSe:CURRent:RANGe:LOWer?')
		return Conversions.str_to_float(response)

	def set_lower(self, arg_0: float) -> None:
		"""SCPI: SENSe:CURRent:RANGe:LOWer \n
		Snippet: driver.sense.current.range.set_lower(arg_0 = 1.0) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SENSe:CURRent:RANGe:LOWer {param}')

	def get_auto(self) -> bool:
		"""SCPI: SENSe:CURRent:RANGe:AUTO \n
		Snippet: value: bool = driver.sense.current.range.get_auto() \n
		Sets or queries auto range for current measurement accuracy. \n
			:return: arg_0: 1 Enables auto range for current. 0 Disables auto range for current.
		"""
		response = self._core.io.query_str('SENSe:CURRent:RANGe:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, arg_0: bool) -> None:
		"""SCPI: SENSe:CURRent:RANGe:AUTO \n
		Snippet: driver.sense.current.range.set_auto(arg_0 = False) \n
		Sets or queries auto range for current measurement accuracy. \n
			:param arg_0: 1 Enables auto range for current. 0 Disables auto range for current.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SENSe:CURRent:RANGe:AUTO {param}')
