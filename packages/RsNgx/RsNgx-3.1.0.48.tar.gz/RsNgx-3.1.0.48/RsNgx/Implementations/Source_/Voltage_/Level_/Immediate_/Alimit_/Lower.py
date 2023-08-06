from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lower:
	"""Lower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lower", core, parent)

	def set(self, voltage: float) -> None:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate]:ALIMit:LOWer \n
		Snippet: driver.source.voltage.level.immediate.alimit.lower.set(voltage = 1.0) \n
		Sets or queries the lower safety limit for voltage. \n
			:param voltage:
				- numeric value: Numeric value for safety limit.
				- MIN | MINimum: Min value for lower safety limit.
				- MAX | MAXimum: Max value for lower safety limit."""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:VOLTage:LEVel:IMMediate:ALIMit:LOWer {param}')

	def get(self) -> float:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate]:ALIMit:LOWer \n
		Snippet: value: float = driver.source.voltage.level.immediate.alimit.lower.get() \n
		Sets or queries the lower safety limit for voltage. \n
			:return: result: No help available"""
		response = self._core.io.query_str(f'SOURce:VOLTage:LEVel:IMMediate:ALIMit:LOWer?')
		return Conversions.str_to_float(response)
