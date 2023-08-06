from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.Types import DataType
from ..Internal.ArgSingleList import ArgSingleList
from ..Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apply:
	"""Apply commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apply", core, parent)

	def set(self, voltage: float, current: float = None, output: int = None) -> None:
		"""SCPI: APPLy \n
		Snippet: driver.apply.set(voltage = 1.0, current = 1.0, output = 1) \n
		Sets or queries the voltage and current value of the selected channel. \n
			:param voltage:
				- numeric: Numeric value for voltage in the range of 0.000 to 64.050.
				- MIN | MINimum: Min voltage at 0.000 V.
				- MAX | MAXimum: Max value for voltage at 64.050V.
				- DEF | DEFault: Default voltage.
			:param current:
				- numeric: Numeric value for current in the range of 0.000 to 20.0100.
				- MIN | MINimum: Min current at 0.000 A.
				- MAX | MAXimum: Max value for current at 0.0100 A.
				- DEF | DEFault: Numeric value for current.
			:param output:
				- OUT1 | OUTP1 | OUTPut1 | CH1: Selects output for channel 1.
				- OUT2 | OUTP2 | OUTPut2 | CH2: Selects output for channel 2.
				- OUT3 | OUTP3 | OUTPut3 | CH3: Selects output for channel 2.
				- OUT4 | OUTP4 | OUTPut4 | CH4: Selects output for channel 4."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('voltage', voltage, DataType.Float), ArgSingle('current', current, DataType.Float, True), ArgSingle('output', output, DataType.Integer, True))
		self._core.io.write(f'APPLy {param}'.rstrip())
