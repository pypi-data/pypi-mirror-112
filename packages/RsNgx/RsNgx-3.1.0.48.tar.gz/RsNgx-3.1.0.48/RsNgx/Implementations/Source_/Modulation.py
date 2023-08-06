from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Modulation_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	def set(self, arg_0: bool, arg_1: str = None) -> None:
		"""SCPI: [SOURce]:MODulation \n
		Snippet: driver.source.modulation.set(arg_0 = False, arg_1 = r1) \n
		No command help available \n
			:param arg_0: No help available
			:param arg_1: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Boolean), ArgSingle('arg_1', arg_1, DataType.RawString, True))
		self._core.io.write(f'SOURce:MODulation {param}'.rstrip())

	def get(self, arg_0: bool, arg_1: str = None) -> bool:
		"""SCPI: [SOURce]:MODulation \n
		Snippet: value: bool = driver.source.modulation.get(arg_0 = False, arg_1 = r1) \n
		No command help available \n
			:param arg_0: No help available
			:param arg_1: No help available
			:return: arg_0: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Boolean), ArgSingle('arg_1', arg_1, DataType.RawString, True))
		response = self._core.io.query_str(f'SOURce:MODulation? {param}'.rstrip())
		return Conversions.str_to_bool(response)
