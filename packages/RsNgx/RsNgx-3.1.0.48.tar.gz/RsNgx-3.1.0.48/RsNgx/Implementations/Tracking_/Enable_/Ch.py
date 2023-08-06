from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ch:
	"""Ch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ch", core, parent)

	def set(self, arg_0: bool, channel=repcap.Channel.Nr1) -> None:
		"""SCPI: TRACking[:ENABle]:CH<CHANNEL> \n
		Snippet: driver.tracking.enable.ch.set(arg_0 = False, channel = repcap.Channel.Nr1) \n
		Sets or queries the tracking status on selected channel. \n
			:param arg_0:
				- 0: Tracking is disabled on specified channel.
				- 1: Tracking is enabled on specified channel.
			:param channel: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.bool_to_str(arg_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACking:ENABle:CH{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Nr1) -> bool:
		"""SCPI: TRACking[:ENABle]:CH<CHANNEL> \n
		Snippet: value: bool = driver.tracking.enable.ch.get(channel = repcap.Channel.Nr1) \n
		Sets or queries the tracking status on selected channel. \n
			:param channel: optional repeated capability selector. Default value: Nr1
			:return: arg_0:
				- 0: Tracking is disabled on specified channel.
				- 1: Tracking is enabled on specified channel."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACking:ENABle:CH{channel_cmd_val}?')
		return Conversions.str_to_bool(response)
