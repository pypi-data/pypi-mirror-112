from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 4 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	@property
	def step(self):
		"""step commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_step'):
			from .Immediate_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def alimit(self):
		"""alimit commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_alimit'):
			from .Immediate_.Alimit import Alimit
			self._alimit = Alimit(self._core, self._base)
		return self._alimit

	def get_amplitude(self) -> float:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: value: float = driver.source.voltage.level.immediate.get_amplitude() \n
		Sets or queries the voltage value of the selected channel. \n
			:return: voltage:
				- numeric value: Numeric value in V.
				- MIN | MINimum: Minimum voltage at 0.000 V.
				- MAX | MAXimum: Maximum voltage at 64.050 V.
				- UP: Increases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement].
				- DOWN: Decreases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]."""
		response = self._core.io.query_str('SOURce:VOLTage:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, voltage: float) -> None:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate][:AMPLitude] \n
		Snippet: driver.source.voltage.level.immediate.set_amplitude(voltage = 1.0) \n
		Sets or queries the voltage value of the selected channel. \n
			:param voltage:
				- numeric value: Numeric value in V.
				- MIN | MINimum: Minimum voltage at 0.000 V.
				- MAX | MAXimum: Maximum voltage at 64.050 V.
				- UP: Increases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement].
				- DOWN: Decreases voltage by a defined step size. See [SOURce:]VOLTage[:LEVel][:IMMediate]:STEP[:INCRement]."""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:VOLTage:LEVel:IMMediate:AMPLitude {param}')
