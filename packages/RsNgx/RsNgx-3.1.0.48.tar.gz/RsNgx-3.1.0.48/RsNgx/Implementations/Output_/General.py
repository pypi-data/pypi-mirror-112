from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class General:
	"""General commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("general", core, parent)

	def get_state(self) -> bool:
		"""SCPI: OUTPut:GENeral[:STATe] \n
		Snippet: value: bool = driver.output.general.get_state() \n
		Sets or queries all previous selected channels simultaneously \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:GENeral:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:GENeral[:STATe] \n
		Snippet: driver.output.general.set_state(arg_0 = False) \n
		Sets or queries all previous selected channels simultaneously \n
			:param arg_0:
				- 0: Switches off previous selected channels simultaneously.
				- 1: Switches on previous selected channels simultaneously."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:GENeral:STATe {param}')
