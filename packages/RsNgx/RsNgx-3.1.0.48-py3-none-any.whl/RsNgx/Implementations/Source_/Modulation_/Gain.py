from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gain:
	"""Gain commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gain", core, parent)

	def set(self, arg_0: float, arg_1: str = None) -> None:
		"""SCPI: [SOURce]:MODulation:GAIN \n
		Snippet: driver.source.modulation.gain.set(arg_0 = 1.0, arg_1 = r1) \n
		Sets or queries the modulation gain. \n
			:param arg_0: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value of the modulation gain. MIN | MINimum Minimum value of the modulation gain. MAX | MAXimum Maximum value of the modulation gain UP Increases gain by a defined step size. DOWN Decreases gain by a defined step size.
			:param arg_1: list
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Float), ArgSingle('arg_1', arg_1, DataType.RawString, True))
		self._core.io.write(f'SOURce:MODulation:GAIN {param}'.rstrip())

	def get(self, arg_0: float, arg_1: str = None) -> float:
		"""SCPI: [SOURce]:MODulation:GAIN \n
		Snippet: value: float = driver.source.modulation.gain.get(arg_0 = 1.0, arg_1 = r1) \n
		Sets or queries the modulation gain. \n
			:param arg_0: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value of the modulation gain. MIN | MINimum Minimum value of the modulation gain. MAX | MAXimum Maximum value of the modulation gain UP Increases gain by a defined step size. DOWN Decreases gain by a defined step size.
			:param arg_1: list
			:return: arg_0: numeric value | MIN | MINimum | MAX | MAXimum | UP | DOWN | list numeric value Numeric value of the modulation gain. MIN | MINimum Minimum value of the modulation gain. MAX | MAXimum Maximum value of the modulation gain UP Increases gain by a defined step size. DOWN Decreases gain by a defined step size."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Float), ArgSingle('arg_1', arg_1, DataType.RawString, True))
		response = self._core.io.query_str(f'SOURce:MODulation:GAIN? {param}'.rstrip())
		return Conversions.str_to_float(response)
