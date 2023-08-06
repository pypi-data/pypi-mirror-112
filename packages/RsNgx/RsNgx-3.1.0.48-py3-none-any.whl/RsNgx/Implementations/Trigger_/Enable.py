from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	@property
	def dio(self):
		"""dio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dio'):
			from .Enable_.Dio import Dio
			self._dio = Dio(self._core, self._base)
		return self._dio

	@property
	def select(self):
		"""select commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_select'):
			from .Enable_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	def get_general(self) -> bool:
		"""SCPI: TRIGger[:ENABle]:GENeral \n
		Snippet: value: bool = driver.trigger.enable.get_general() \n
		Sets or queries the enable state of the master on/off of Digital I/O trigger. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('TRIGger:ENABle:GENeral?')
		return Conversions.str_to_bool(response)

	def set_general(self, arg_0: bool) -> None:
		"""SCPI: TRIGger[:ENABle]:GENeral \n
		Snippet: driver.trigger.enable.set_general(arg_0 = False) \n
		Sets or queries the enable state of the master on/off of Digital I/O trigger. \n
			:param arg_0:
				- 1: Master state of Digital I/O trigger is enabled.
				- 0: Master state of Digital I/O trigger is disabled."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'TRIGger:ENABle:GENeral {param}')
