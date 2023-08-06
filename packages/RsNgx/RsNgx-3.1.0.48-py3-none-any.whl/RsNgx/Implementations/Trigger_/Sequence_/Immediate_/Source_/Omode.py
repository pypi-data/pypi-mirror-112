from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Omode:
	"""Omode commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("omode", core, parent)

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Omode_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	def set(self, arg_0: enums.TriggerOperMode) -> None:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:OMODe \n
		Snippet: driver.trigger.sequence.immediate.source.omode.set(arg_0 = enums.TriggerOperMode.CC) \n
		Sets or queries the operation mode to trigger on for trigger source 'operation mode' See Figure 'Overview of trigger IO
		system'. \n
			:param arg_0: CC | CV | CR | SINK | PROTection CC If respective channel operation mode is detected in CC mode, corresponding trigger-out parameters are triggered. CV If respective channel operation mode is detected in CV mode, corresponding trigger-out parameters are triggered. CR If respective channel operation mode is detected in CR mode, corresponding trigger-out parameters are triggered. SINK If respective channel operation mode is detected in sink mode, corresponding trigger-out parameters are triggered. PROTection If respective channel operation mode is detected in protection mode (OVP, OCP, OPP OTP) , corresponding trigger-out parameters are triggered.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerOperMode)
		self._core.io.write(f'TRIGger:SEQuence:IMMediate:SOURce:OMODe {param}')

	# noinspection PyTypeChecker
	def get(self, arg_0: enums.TriggerOperMode) -> enums.TriggerOperMode:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce:OMODe \n
		Snippet: value: enums.TriggerOperMode = driver.trigger.sequence.immediate.source.omode.get(arg_0 = enums.TriggerOperMode.CC) \n
		Sets or queries the operation mode to trigger on for trigger source 'operation mode' See Figure 'Overview of trigger IO
		system'. \n
			:param arg_0: CC | CV | CR | SINK | PROTection CC If respective channel operation mode is detected in CC mode, corresponding trigger-out parameters are triggered. CV If respective channel operation mode is detected in CV mode, corresponding trigger-out parameters are triggered. CR If respective channel operation mode is detected in CR mode, corresponding trigger-out parameters are triggered. SINK If respective channel operation mode is detected in sink mode, corresponding trigger-out parameters are triggered. PROTection If respective channel operation mode is detected in protection mode (OVP, OCP, OPP OTP) , corresponding trigger-out parameters are triggered.
			:return: arg_0: CC | CV | CR | SINK | PROTection CC If respective channel operation mode is detected in CC mode, corresponding trigger-out parameters are triggered. CV If respective channel operation mode is detected in CV mode, corresponding trigger-out parameters are triggered. CR If respective channel operation mode is detected in CR mode, corresponding trigger-out parameters are triggered. SINK If respective channel operation mode is detected in sink mode, corresponding trigger-out parameters are triggered. PROTection If respective channel operation mode is detected in protection mode (OVP, OCP, OPP OTP) , corresponding trigger-out parameters are triggered."""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerOperMode)
		response = self._core.io.query_str(f'TRIGger:SEQuence:IMMediate:SOURce:OMODe? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TriggerOperMode)
