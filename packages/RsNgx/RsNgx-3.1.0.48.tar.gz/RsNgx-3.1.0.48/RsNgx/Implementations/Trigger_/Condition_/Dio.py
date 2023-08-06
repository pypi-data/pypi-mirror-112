from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
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

	# noinspection PyTypeChecker
	class DioStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Arg_0: enums.TriggerCondition: No parameter help available
			- Arg_1: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Arg_0', enums.TriggerCondition),
			ArgStruct.scalar_float('Arg_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Arg_0: enums.TriggerCondition = None
			self.Arg_1: float = None

	def set(self, structure: DioStruct, digitalIo=repcap.DigitalIo.Default) -> None:
		"""SCPI: TRIGger:CONDition:DIO<IO> \n
		Snippet: driver.trigger.condition.dio.set(value = [PROPERTY_STRUCT_NAME](), digitalIo = repcap.DigitalIo.Default) \n
		Sets the trigger condition of the specified Digital I/O line. \n
			:param structure: for set value, see the help for DioStruct structure arguments.
			:param digitalIo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dio')"""
		digitalIo_cmd_val = self._base.get_repcap_cmd_value(digitalIo, repcap.DigitalIo)
		self._core.io.write_struct(f'TRIGger:CONDition:DIO{digitalIo_cmd_val}', structure)

	def get(self, digitalIo=repcap.DigitalIo.Default) -> DioStruct:
		"""SCPI: TRIGger:CONDition:DIO<IO> \n
		Snippet: value: DioStruct = driver.trigger.condition.dio.get(digitalIo = repcap.DigitalIo.Default) \n
		Sets the trigger condition of the specified Digital I/O line. \n
			:param digitalIo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dio')
			:return: structure: for return value, see the help for DioStruct structure arguments."""
		digitalIo_cmd_val = self._base.get_repcap_cmd_value(digitalIo, repcap.DigitalIo)
		return self._core.io.query_struct(f'TRIGger:CONDition:DIO{digitalIo_cmd_val}?', self.__class__.DioStruct())
