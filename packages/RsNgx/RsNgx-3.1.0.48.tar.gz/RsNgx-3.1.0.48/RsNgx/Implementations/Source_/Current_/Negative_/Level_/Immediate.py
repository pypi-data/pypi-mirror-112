from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def get_amplitude(self) -> float:
		"""SCPI: SOURce:CURRent:NEGative[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: value: float = driver.source.current.negative.level.immediate.get_amplitude() \n
		Sets or queries the negative current value. \n
			:return: current: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value in the range of 0.000 to 20.0100 . MIN | MINimum Minimum current at 0.0005 A. MAX | MAXimum Depending on the set voltage level, the maximum set current is 20.0100 A. For voltage range up to 32 V, maximum set current is 20.0100 A. For voltage range up to 64 V, maximum set current is 10.0100 A. UP Increases current by a defined step size. See [SOURce:]CURRent[:LEVel][:IMMediate]:STEP[:INCRement]. DOWN Decreases current by a defined step size. See [SOURce:]CURRent[:LEVel][:IMMediate]:STEP[:INCRement].
		"""
		response = self._core.io.query_str('SOURce:CURRent:NEGative:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, current: float) -> None:
		"""SCPI: SOURce:CURRent:NEGative[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: driver.source.current.negative.level.immediate.set_amplitude(current = 1.0) \n
		Sets or queries the negative current value. \n
			:param current: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value in the range of 0.000 to 20.0100 . MIN | MINimum Minimum current at 0.0005 A. MAX | MAXimum Depending on the set voltage level, the maximum set current is 20.0100 A. For voltage range up to 32 V, maximum set current is 20.0100 A. For voltage range up to 64 V, maximum set current is 10.0100 A. UP Increases current by a defined step size. See [SOURce:]CURRent[:LEVel][:IMMediate]:STEP[:INCRement]. DOWN Decreases current by a defined step size. See [SOURce:]CURRent[:LEVel][:IMMediate]:STEP[:INCRement].
		"""
		param = Conversions.decimal_value_to_str(current)
		self._core.io.write(f'SOURce:CURRent:NEGative:LEVel:IMMediate:AMPLitude {param}')
