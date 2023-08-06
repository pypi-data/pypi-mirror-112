from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, arg_0: bool) -> None:
		"""SCPI: TRIGger[:STATe] \n
		Snippet: driver.trigger.state.set(arg_0 = False) \n
		Enables or disables the trigger system. Upon being triggered, the selected trigger source method RsNgx.Trigger.Sequence.
		Immediate.Source.set becomes active. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: 1 Enables the trigger system. 0 Disables the trigger system.
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'TRIGger:STATe {param}')

	def get(self) -> bool:
		"""SCPI: TRIGger[:STATe] \n
		Snippet: value: bool = driver.trigger.state.get() \n
		Enables or disables the trigger system. Upon being triggered, the selected trigger source method RsNgx.Trigger.Sequence.
		Immediate.Source.set becomes active. See Figure 'Overview of trigger IO system'. \n
			:return: arg_0: 1 Enables the trigger system. 0 Disables the trigger system."""
		response = self._core.io.query_str(f'TRIGger:STATe?')
		return Conversions.str_to_bool(response)
