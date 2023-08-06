from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)

	def set(self, arg_0: int) -> None:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:DIO:CHANnel \n
		Snippet: driver.trigger.sequence.immediate.source.dio.channel.set(arg_0 = 1) \n
		Sets or queries the device channel for trigger source 'Digital In Channel'. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: OUT1 | OUTP1 | OUTPut1 | OUT2 | OUTP2 | OUTPut2 OUT1 | OUTP1 | OUTPut1 Ch1 is selected as the device channel for trigger source. OUT2 | OUTP2 | OUTPut2 Ch2 is selected as the device channel for trigger source.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'TRIGger:SEQuence:IMMediate:SOURce:DIO:CHANnel {param}')

	def get(self, arg_0: int) -> int:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:DIO:CHANnel \n
		Snippet: value: int = driver.trigger.sequence.immediate.source.dio.channel.get(arg_0 = 1) \n
		Sets or queries the device channel for trigger source 'Digital In Channel'. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: OUT1 | OUTP1 | OUTPut1 | OUT2 | OUTP2 | OUTPut2 OUT1 | OUTP1 | OUTPut1 Ch1 is selected as the device channel for trigger source. OUT2 | OUTP2 | OUTPut2 Ch2 is selected as the device channel for trigger source.
			:return: arg_0: OUT1 | OUTP1 | OUTPut1 | OUT2 | OUTP2 | OUTPut2 OUT1 | OUTP1 | OUTPut1 Ch1 is selected as the device channel for trigger source. OUT2 | OUTP2 | OUTPut2 Ch2 is selected as the device channel for trigger source."""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str(f'TRIGger:SEQuence:IMMediate:SOURce:DIO:CHANnel? {param}')
		return Conversions.str_to_int(response)
