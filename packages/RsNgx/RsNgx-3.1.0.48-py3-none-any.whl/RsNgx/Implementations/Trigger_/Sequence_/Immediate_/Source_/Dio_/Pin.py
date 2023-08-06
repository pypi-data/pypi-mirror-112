from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pin:
	"""Pin commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pin", core, parent)

	def set(self, arg_0: enums.TriggerDioSource) -> None:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:DIO:PIN \n
		Snippet: driver.trigger.sequence.immediate.source.dio.pin.set(arg_0 = enums.TriggerDioSource.EXT) \n
		Sets or queries the DIO pin to trigger on for trigger source 'Digital In Channel'. See Figure 'Overview of trigger IO
		system'. \n
			:param arg_0: IN | EXT IN Pin 3 of DIO connector is monitored. EXT Pin 2 (Ch1) of DIO connector is monitored.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerDioSource)
		self._core.io.write(f'TRIGger:SEQuence:IMMediate:SOURce:DIO:PIN {param}')

	# noinspection PyTypeChecker
	def get(self, arg_0: enums.TriggerDioSource) -> enums.TriggerDioSource:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:DIO:PIN \n
		Snippet: value: enums.TriggerDioSource = driver.trigger.sequence.immediate.source.dio.pin.get(arg_0 = enums.TriggerDioSource.EXT) \n
		Sets or queries the DIO pin to trigger on for trigger source 'Digital In Channel'. See Figure 'Overview of trigger IO
		system'. \n
			:param arg_0: IN | EXT IN Pin 3 of DIO connector is monitored. EXT Pin 2 (Ch1) of DIO connector is monitored.
			:return: arg_0: IN | EXT IN Pin 3 of DIO connector is monitored. EXT Pin 2 (Ch1) of DIO connector is monitored."""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerDioSource)
		response = self._core.io.query_str(f'TRIGger:SEQuence:IMMediate:SOURce:DIO:PIN? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TriggerDioSource)
