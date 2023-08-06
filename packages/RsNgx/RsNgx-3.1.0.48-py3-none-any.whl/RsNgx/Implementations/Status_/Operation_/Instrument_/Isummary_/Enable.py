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
		"""SCPI: STATus:OPERation:INSTrument:ISUMmary<Channel>:ENABle \n
		Snippet: driver.status.operation.instrument.isummary.enable.set(arg_0 = 1, channel = repcap.Channel.Default) \n
		Controls or queries the ENABle part of the STATus:OPERation register. The ENABle defines which events in the EVENt part
		of the status register are forwarded to the OPERation summary bit (bit 7) of the status byte. The status byte can be used
		to create a service request. \n
			:param arg_0: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')"""
		param = Conversions.decimal_value_to_str(arg_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'STATus:OPERation:INSTrument:ISUMmary{channel_cmd_val}:ENABle {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: STATus:OPERation:INSTrument:ISUMmary<Channel>:ENABle \n
		Snippet: value: int = driver.status.operation.instrument.isummary.enable.get(channel = repcap.Channel.Default) \n
		Controls or queries the ENABle part of the STATus:OPERation register. The ENABle defines which events in the EVENt part
		of the status register are forwarded to the OPERation summary bit (bit 7) of the status byte. The status byte can be used
		to create a service request. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')
			:return: arg_0: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'STATus:OPERation:INSTrument:ISUMmary{channel_cmd_val}:ENABle?')
		return Conversions.str_to_int(response)
