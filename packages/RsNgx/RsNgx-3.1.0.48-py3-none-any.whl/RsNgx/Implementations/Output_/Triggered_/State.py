from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:TRIGgered[:STATe] \n
		Snippet: driver.output.triggered.state.set(arg_0 = False) \n
		Enables or disables the triggered event for output. \n
			:param arg_0: 1 Trigger is enabled. 0 Trigger is disabled.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:TRIGgered:STATe {param}')

	def get(self) -> bool:
		"""SCPI: OUTPut:TRIGgered[:STATe] \n
		Snippet: value: bool = driver.output.triggered.state.get() \n
		Enables or disables the triggered event for output. \n
			:return: arg_0: 1 Trigger is enabled. 0 Trigger is disabled."""
		response = self._core.io.query_str_with_opc(f'OUTPut:TRIGgered:STATe?')
		return Conversions.str_to_bool(response)
