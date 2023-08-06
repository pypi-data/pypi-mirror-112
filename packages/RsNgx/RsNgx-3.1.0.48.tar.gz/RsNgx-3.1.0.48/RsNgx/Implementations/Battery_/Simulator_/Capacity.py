from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Capacity:
	"""Capacity commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("capacity", core, parent)

	def get_limit(self) -> float:
		"""SCPI: BATTery:SIMulator:CAPacity:LIMit \n
		Snippet: value: float = driver.battery.simulator.capacity.get_limit() \n
		Sets or queries the full battery capacity. \n
			:return: arg_0: Defines the full battery capacity.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CAPacity:LIMit?')
		return Conversions.str_to_float(response)

	def set_limit(self, arg_0: float) -> None:
		"""SCPI: BATTery:SIMulator:CAPacity:LIMit \n
		Snippet: driver.battery.simulator.capacity.set_limit(arg_0 = 1.0) \n
		Sets or queries the full battery capacity. \n
			:param arg_0: Defines the full battery capacity.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:CAPacity:LIMit {param}')

	def get_value(self) -> float:
		"""SCPI: BATTery:SIMulator:CAPacity \n
		Snippet: value: float = driver.battery.simulator.capacity.get_value() \n
		Queries the remaining battery capacity. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CAPacity?')
		return Conversions.str_to_float(response)
