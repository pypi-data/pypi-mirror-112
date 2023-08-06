from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Behavior:
	"""Behavior commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("behavior", core, parent)

	# noinspection PyTypeChecker
	def get_end(self) -> enums.ArbEndBehavior:
		"""SCPI: ARBitrary:BEHavior:END \n
		Snippet: value: enums.ArbEndBehavior = driver.arbitrary.behavior.get_end() \n
		Sets or queries the arbitrary endpoint behavior, when arbitrary function is finished. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('ARBitrary:BEHavior:END?')
		return Conversions.str_to_scalar_enum(response, enums.ArbEndBehavior)

	def set_end(self, arg_0: enums.ArbEndBehavior) -> None:
		"""SCPI: ARBitrary:BEHavior:END \n
		Snippet: driver.arbitrary.behavior.set_end(arg_0 = enums.ArbEndBehavior.HOLD) \n
		Sets or queries the arbitrary endpoint behavior, when arbitrary function is finished. \n
			:param arg_0: HOLD | OFF OFF If the arbitrary function is finished, the respective channel is deactivated automatically. HOLD If the arbitrary function is finished, the last arbitrary point of the user-defined arbitrary list is held.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.ArbEndBehavior)
		self._core.io.write(f'ARBitrary:BEHavior:END {param}')
