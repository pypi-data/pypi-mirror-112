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
		"""SCPI: SOURce:VOLTage:NEGative[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: value: float = driver.source.voltage.negative.level.immediate.get_amplitude() \n
		Sets or queries the negative voltage value. Applicable only with NGU401 model. \n
			:return: voltage: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value in V. MIN | MINimum Minimum voltage at 0.000 V. MAX | MAXimum Maximum voltage at 64.050 V. UP Increases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]. DOWN Decreases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]. Range: 0.000 to 64.050
		"""
		response = self._core.io.query_str('SOURce:VOLTage:NEGative:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, voltage: float) -> None:
		"""SCPI: SOURce:VOLTage:NEGative[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: driver.source.voltage.negative.level.immediate.set_amplitude(voltage = 1.0) \n
		Sets or queries the negative voltage value. Applicable only with NGU401 model. \n
			:param voltage: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value in V. MIN | MINimum Minimum voltage at 0.000 V. MAX | MAXimum Maximum voltage at 64.050 V. UP Increases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]. DOWN Decreases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]. Range: 0.000 to 64.050
		"""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:VOLTage:NEGative:LEVel:IMMediate:AMPLitude {param}')
