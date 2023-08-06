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
	def ch(self):
		"""ch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ch'):
			from .Enable_.Ch import Ch
			self._ch = Ch(self._core, self._base)
		return self._ch

	@property
	def select(self):
		"""select commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_select'):
			from .Enable_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	def get_general(self) -> bool:
		"""SCPI: TRACking[:ENABle]:GENeral \n
		Snippet: value: bool = driver.tracking.enable.get_general() \n
		Sets or queries the status of the master tracking state. \n
			:return: arg_0:
				- 0: Master tracking is disabled
				- 1: Master tracking is enabled"""
		response = self._core.io.query_str('TRACking:ENABle:GENeral?')
		return Conversions.str_to_bool(response)

	def set_general(self, arg_0: bool) -> None:
		"""SCPI: TRACking[:ENABle]:GENeral \n
		Snippet: driver.tracking.enable.set_general(arg_0 = False) \n
		Sets or queries the status of the master tracking state. \n
			:param arg_0:
				- 0: Master tracking is disabled
				- 1: Master tracking is enabled"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'TRACking:ENABle:GENeral {param}')
