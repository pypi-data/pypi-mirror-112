from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NplCycles:
	"""NplCycles commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nplCycles", core, parent)

	def set(self, arg_0: float, arg_1: str = None) -> None:
		"""SCPI: [SENSe]:NPLCycles \n
		Snippet: driver.sense.nplCycles.set(arg_0 = 1.0, arg_1 = r1) \n
		Sets or queries the number of power line cycles for measurements. \n
			:param arg_0: Number of power line cycles for measurements.
			:param arg_1: list
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Float), ArgSingle('arg_1', arg_1, DataType.RawString, True))
		self._core.io.write(f'SENSe:NPLCycles {param}'.rstrip())

	def get(self, arg_1: str = None) -> float:
		"""SCPI: [SENSe]:NPLCycles \n
		Snippet: value: float = driver.sense.nplCycles.get(arg_1 = r1) \n
		Sets or queries the number of power line cycles for measurements. \n
			:param arg_1: list
			:return: arg_0: Number of power line cycles for measurements."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_1', arg_1, DataType.RawString, True))
		response = self._core.io.query_str(f'SENSe:NPLCycles? {param}'.rstrip())
		return Conversions.str_to_float(response)
