from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Increment:
	"""Increment commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("increment", core, parent)

	def set(self, desired_stepsize: float, optional_default_step_query: enums.DefaultStep = None) -> None:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate]:STEP[:INCRement] \n
		Snippet: driver.source.voltage.level.immediate.step.increment.set(desired_stepsize = 1.0, optional_default_step_query = enums.DefaultStep.DEF) \n
		Sets or queries the incremental step size for the [SOURce:]VOLTage[:LEVel][:IMMediate][:AMPLitude] command. \n
			:param desired_stepsize: No help available
			:param optional_default_step_query: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('desired_stepsize', desired_stepsize, DataType.Float), ArgSingle('optional_default_step_query', optional_default_step_query, DataType.Enum, True))
		self._core.io.write(f'SOURce:VOLTage:LEVel:IMMediate:STEP:INCRement {param}'.rstrip())

	def get(self, optional_default_step_query: enums.DefaultStep = None) -> float:
		"""SCPI: [SOURce]:VOLTage[:LEVel][:IMMediate]:STEP[:INCRement] \n
		Snippet: value: float = driver.source.voltage.level.immediate.step.increment.get(optional_default_step_query = enums.DefaultStep.DEF) \n
		Sets or queries the incremental step size for the [SOURce:]VOLTage[:LEVel][:IMMediate][:AMPLitude] command. \n
			:param optional_default_step_query: No help available
			:return: result: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('optional_default_step_query', optional_default_step_query, DataType.Enum, True))
		response = self._core.io.query_str(f'SOURce:VOLTage:LEVel:IMMediate:STEP:INCRement? {param}'.rstrip())
		return Conversions.str_to_float(response)
