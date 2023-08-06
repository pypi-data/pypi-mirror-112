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
		"""SCPI: SENSe:VOLTage:RANGe[:UPPer] \n
		Snippet: value: float = driver.sense.voltage.range.get_upper() \n
		Sets or queries the voltage range for measurement. There is a selection of 20 V and 5 V range. \n
			:return: arg_0: Defines the voltage range for measurement (20 V and 5 V) . Unit: V
		"""
		response = self._core.io.query_str('SENSe:VOLTage:RANGe:UPPer?')
		return Conversions.str_to_float(response)

	def set_upper(self, arg_0: float) -> None:
		"""SCPI: SENSe:VOLTage:RANGe[:UPPer] \n
		Snippet: driver.sense.voltage.range.set_upper(arg_0 = 1.0) \n
		Sets or queries the voltage range for measurement. There is a selection of 20 V and 5 V range. \n
			:param arg_0: Defines the voltage range for measurement (20 V and 5 V) . Unit: V
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SENSe:VOLTage:RANGe:UPPer {param}')

	def get_lower(self) -> float:
		"""SCPI: SENSe:VOLTage:RANGe:LOWer \n
		Snippet: value: float = driver.sense.voltage.range.get_lower() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SENSe:VOLTage:RANGe:LOWer?')
		return Conversions.str_to_float(response)

	def set_lower(self, arg_0: float) -> None:
		"""SCPI: SENSe:VOLTage:RANGe:LOWer \n
		Snippet: driver.sense.voltage.range.set_lower(arg_0 = 1.0) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SENSe:VOLTage:RANGe:LOWer {param}')

	def get_auto(self) -> bool:
		"""SCPI: SENSe:VOLTage:RANGe:AUTO \n
		Snippet: value: bool = driver.sense.voltage.range.get_auto() \n
		Sets or queries auto range for voltage measurement accuracy. \n
			:return: arg_0: 1 Enables auto range for voltage. 0 Disables auto range for voltage.
		"""
		response = self._core.io.query_str('SENSe:VOLTage:RANGe:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, arg_0: bool) -> None:
		"""SCPI: SENSe:VOLTage:RANGe:AUTO \n
		Snippet: driver.sense.voltage.range.set_auto(arg_0 = False) \n
		Sets or queries auto range for voltage measurement accuracy. \n
			:param arg_0: 1 Enables auto range for voltage. 0 Disables auto range for voltage.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'SENSe:VOLTage:RANGe:AUTO {param}')
