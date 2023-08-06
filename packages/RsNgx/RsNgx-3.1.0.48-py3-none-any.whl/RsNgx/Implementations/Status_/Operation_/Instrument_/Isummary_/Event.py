from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Event:
	"""Event commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("event", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: STATus:OPERation:INSTrument:ISUMmary<Channel>[:EVENt] \n
		Snippet: value: int = driver.status.operation.instrument.isummary.event.get(channel = repcap.Channel.Default) \n
		Returns the contents of the EVENt part of the status register to check whether an event has occurred since the last
		reading. Reading an EVENt register deletes its contents. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')
			:return: result: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'STATus:OPERation:INSTrument:ISUMmary{channel_cmd_val}:EVENt?')
		return Conversions.str_to_int(response)
