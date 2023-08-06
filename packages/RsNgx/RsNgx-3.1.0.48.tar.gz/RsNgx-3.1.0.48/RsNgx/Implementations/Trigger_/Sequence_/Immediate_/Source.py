from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 6 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	@property
	def output(self):
		"""output commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Source_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def omode(self):
		"""omode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_omode'):
			from .Source_.Omode import Omode
			self._omode = Omode(self._core, self._base)
		return self._omode

	@property
	def dio(self):
		"""dio commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dio'):
			from .Source_.Dio import Dio
			self._dio = Dio(self._core, self._base)
		return self._dio

	def set(self, arg_0: enums.TriggerSource) -> None:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce \n
		Snippet: driver.trigger.sequence.immediate.source.set(arg_0 = enums.TriggerSource.DIO) \n
		Sets or queries the trigger source. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: OUTPut | OMODe | DIO OUTPut Trigger source is from the output channel. OMODe Trigger source is from the different modes (CC, CR, CV, Sink, OVP, OCP, OPP and OTP) detected from the output channel. DIO Trigger source is from DIO connector at the instrument rear panel.
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerSource)
		self._core.io.write(f'TRIGger:SEQuence:IMMediate:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, arg_0: enums.TriggerSource) -> enums.TriggerSource:
		"""SCPI: TRIGger[:SEQuence][:IMMediate]:SOURce \n
		Snippet: value: enums.TriggerSource = driver.trigger.sequence.immediate.source.get(arg_0 = enums.TriggerSource.DIO) \n
		Sets or queries the trigger source. See Figure 'Overview of trigger IO system'. \n
			:param arg_0: OUTPut | OMODe | DIO OUTPut Trigger source is from the output channel. OMODe Trigger source is from the different modes (CC, CR, CV, Sink, OVP, OCP, OPP and OTP) detected from the output channel. DIO Trigger source is from DIO connector at the instrument rear panel.
			:return: arg_0: OUTPut | OMODe | DIO OUTPut Trigger source is from the output channel. OMODe Trigger source is from the different modes (CC, CR, CV, Sink, OVP, OCP, OPP and OTP) detected from the output channel. DIO Trigger source is from DIO connector at the instrument rear panel."""
		param = Conversions.enum_scalar_to_str(arg_0, enums.TriggerSource)
		response = self._core.io.query_str(f'TRIGger:SEQuence:IMMediate:SOURce? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSource)
