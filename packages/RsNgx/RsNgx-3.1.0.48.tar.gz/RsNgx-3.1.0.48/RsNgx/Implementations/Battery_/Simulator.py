from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Simulator:
	"""Simulator commands group definition. 14 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("simulator", core, parent)

	@property
	def voc(self):
		"""voc commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_voc'):
			from .Simulator_.Voc import Voc
			self._voc = Voc(self._core, self._base)
		return self._voc

	@property
	def capacity(self):
		"""capacity commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_capacity'):
			from .Simulator_.Capacity import Capacity
			self._capacity = Capacity(self._core, self._base)
		return self._capacity

	@property
	def current(self):
		"""current commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .Simulator_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	def get_enable(self) -> bool:
		"""SCPI: BATTery:SIMulator[:ENABle] \n
		Snippet: value: bool = driver.battery.simulator.get_enable() \n
		Sets or queries the battery simulator state. \n
			:return: arg_0: 1 Enables the battery simulator state. 0 Disables the battery simulator state.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, arg_0: bool) -> None:
		"""SCPI: BATTery:SIMulator[:ENABle] \n
		Snippet: driver.battery.simulator.set_enable(arg_0 = False) \n
		Sets or queries the battery simulator state. \n
			:param arg_0: 1 Enables the battery simulator state. 0 Disables the battery simulator state.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:ENABle {param}')

	def get_soc(self) -> float:
		"""SCPI: BATTery:SIMulator:SOC \n
		Snippet: value: float = driver.battery.simulator.get_soc() \n
		Sets or queries the state of charge (SoC) of the battery simulator. \n
			:return: arg_0: Sets SoC values.
		"""
		response = self._core.io.query_str('BATTery:SIMulator:SOC?')
		return Conversions.str_to_float(response)

	def set_soc(self, arg_0: float) -> None:
		"""SCPI: BATTery:SIMulator:SOC \n
		Snippet: driver.battery.simulator.set_soc(arg_0 = 1.0) \n
		Sets or queries the state of charge (SoC) of the battery simulator. \n
			:param arg_0: Sets SoC values.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'BATTery:SIMulator:SOC {param}')

	def get_resistance(self) -> float:
		"""SCPI: BATTery:SIMulator:RESistance \n
		Snippet: value: float = driver.battery.simulator.get_resistance() \n
		Queries the battery simulator internal resistance (ESR) . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:RESistance?')
		return Conversions.str_to_float(response)

	def get_tvoltage(self) -> float:
		"""SCPI: BATTery:SIMulator:TVOLtage \n
		Snippet: value: float = driver.battery.simulator.get_tvoltage() \n
		Queries the terminal voltage (Vt) . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:TVOLtage?')
		return Conversions.str_to_float(response)
