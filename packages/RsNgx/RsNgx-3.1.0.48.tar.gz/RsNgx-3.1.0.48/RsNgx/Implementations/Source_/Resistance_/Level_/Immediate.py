from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def get_amplitude(self) -> float:
		"""SCPI: [SOURce]:RESistance[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: value: float = driver.source.resistance.level.immediate.get_amplitude() \n
		Sets or queries the constant resistance target value. \n
			:return: current: No help available
		"""
		response = self._core.io.query_str('SOURce:RESistance:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, current: float) -> None:
		"""SCPI: [SOURce]:RESistance[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: driver.source.resistance.level.immediate.set_amplitude(current = 1.0) \n
		Sets or queries the constant resistance target value. \n
			:param current: No help available
		"""
		param = Conversions.decimal_value_to_str(current)
		self._core.io.write(f'SOURce:RESistance:LEVel:IMMediate:AMPLitude {param}')
