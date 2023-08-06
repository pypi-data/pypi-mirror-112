from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Priority:
	"""Priority commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("priority", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PrioMode:
		"""SCPI: ARBitrary:PRIority:MODE \n
		Snippet: value: enums.PrioMode = driver.arbitrary.priority.get_mode() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:PRIority:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PrioMode)

	def set_mode(self, arg_0: enums.PrioMode) -> None:
		"""SCPI: ARBitrary:PRIority:MODE \n
		Snippet: driver.arbitrary.priority.set_mode(arg_0 = enums.PrioMode.CPM) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.PrioMode)
		self._core.io.write(f'ARBitrary:PRIority:MODE {param}')
