from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dio:
	"""Dio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: DigitalIo, default value after init: DigitalIo.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dio", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_digitalIo_get', 'repcap_digitalIo_set', repcap.DigitalIo.Nr1)

	def repcap_digitalIo_set(self, enum_value: repcap.DigitalIo) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to DigitalIo.Default
		Default value after init: DigitalIo.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_digitalIo_get(self) -> repcap.DigitalIo:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, arg_0: bool, digitalIo=repcap.DigitalIo.Default) -> None:
		"""SCPI: TRIGger[:ENABle]:DIO<IO> \n
		Snippet: driver.trigger.enable.dio.set(arg_0 = False, digitalIo = repcap.DigitalIo.Default) \n
		Sets or queries the enable state of the specified Digital I/O line. \n
			:param arg_0:
				- 1: Selected Digital /O line is enabled.
				- 0: Selected Digital /O line is disabled.
			:param digitalIo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dio')"""
		param = Conversions.bool_to_str(arg_0)
		digitalIo_cmd_val = self._base.get_repcap_cmd_value(digitalIo, repcap.DigitalIo)
		self._core.io.write(f'TRIGger:ENABle:DIO{digitalIo_cmd_val} {param}')

	def get(self, digitalIo=repcap.DigitalIo.Default) -> bool:
		"""SCPI: TRIGger[:ENABle]:DIO<IO> \n
		Snippet: value: bool = driver.trigger.enable.dio.get(digitalIo = repcap.DigitalIo.Default) \n
		Sets or queries the enable state of the specified Digital I/O line. \n
			:param digitalIo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dio')
			:return: arg_0: No help available"""
		digitalIo_cmd_val = self._base.get_repcap_cmd_value(digitalIo, repcap.DigitalIo)
		response = self._core.io.query_str(f'TRIGger:ENABle:DIO{digitalIo_cmd_val}?')
		return Conversions.str_to_bool(response)
