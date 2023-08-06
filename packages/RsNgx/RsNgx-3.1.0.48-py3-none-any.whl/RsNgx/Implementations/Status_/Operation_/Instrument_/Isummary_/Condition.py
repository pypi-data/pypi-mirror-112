from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Condition:
	"""Condition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("condition", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: STATus:OPERation:INSTrument:ISUMmary<Channel>:CONDition \n
		Snippet: value: int = driver.status.operation.instrument.isummary.condition.get(channel = repcap.Channel.Default) \n
		Returns the contents of the CONDition part of the status register to check for operation instrument or measurement states.
		Reading the CONDition registers does not delete the contents. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Isummary')
			:return: result: Condition bits in decimal representation."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'STATus:OPERation:INSTrument:ISUMmary{channel_cmd_val}:CONDition?')
		return Conversions.str_to_int(response)
