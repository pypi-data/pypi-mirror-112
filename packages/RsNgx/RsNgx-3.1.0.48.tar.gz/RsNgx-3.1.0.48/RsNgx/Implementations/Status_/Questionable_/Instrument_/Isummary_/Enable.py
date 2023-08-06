from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, arg_0: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: STATus:QUEStionable:INSTrument:ISUMmary<Channel>:ENABle \n
		Snippet: driver.status.questionable.instrument.isummary.enable.set(arg_0 = 1, channel = repcap.Channel.Default) \n
		Sets or queries the enable mask that allows true conditions in the EVENt part to be reported in the summary bit. If a bit
		in the ENABle part is 1, and the corresponding EVENt bit is true, a positive transition occurs in the summary bit. This
		transition is reported to the next higher level. \n
			:param arg_0: Bit mask in decimal representation
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')"""
		param = Conversions.decimal_value_to_str(arg_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'STATus:QUEStionable:INSTrument:ISUMmary{channel_cmd_val}:ENABle {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:ISUMmary<Channel>:ENABle \n
		Snippet: value: int = driver.status.questionable.instrument.isummary.enable.get(channel = repcap.Channel.Default) \n
		Sets or queries the enable mask that allows true conditions in the EVENt part to be reported in the summary bit. If a bit
		in the ENABle part is 1, and the corresponding EVENt bit is true, a positive transition occurs in the summary bit. This
		transition is reported to the next higher level. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')
			:return: arg_0: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'STATus:QUEStionable:INSTrument:ISUMmary{channel_cmd_val}:ENABle?')
		return Conversions.str_to_int(response)
