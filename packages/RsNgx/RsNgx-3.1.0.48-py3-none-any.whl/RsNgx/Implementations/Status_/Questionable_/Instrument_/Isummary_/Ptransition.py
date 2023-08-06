from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptransition:
	"""Ptransition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptransition", core, parent)

	def set(self, arg_0: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: STATus:QUEStionable:INSTrument:ISUMmary<Channel>:PTRansition \n
		Snippet: driver.status.questionable.instrument.isummary.ptransition.set(arg_0 = 1, channel = repcap.Channel.Default) \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param arg_0: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')"""
		param = Conversions.decimal_value_to_str(arg_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'STATus:QUEStionable:INSTrument:ISUMmary{channel_cmd_val}:PTRansition {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:ISUMmary<Channel>:PTRansition \n
		Snippet: value: int = driver.status.questionable.instrument.isummary.ptransition.get(channel = repcap.Channel.Default) \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')
			:return: arg_0: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'STATus:QUEStionable:INSTrument:ISUMmary{channel_cmd_val}:PTRansition?')
		return Conversions.str_to_int(response)
