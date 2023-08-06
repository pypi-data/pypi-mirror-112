from typing import List

from .Internal.Core import Core
from .Internal.InstrumentErrors import RsInstrException
from .Internal.CommandsGroup import CommandsGroup
from .Internal.VisaSession import VisaSession
from .Internal.StructBase import StructBase
from .Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsNgx:
	"""289 total commands, 21 Sub-groups, 1 group commands"""
	_driver_options = "SupportedInstrModels = NGP/NGL/NGM/NGU, SupportedIdnPatterns = NGP/NGL/NGM/NGU, SimulationIdnString = 'Rohde&Schwarz,NGP,100001,3.1.0.0048'"

	def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsNgx session. \n
		Parameter options tokens examples:
			- ``Simulate=True`` - starts the session in simulation mode. Default: ``False``
			- ``SelectVisa=socket`` - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- ``SelectVisa=rs`` - forces usage of RohdeSchwarz Visa
			- ``SelectVisa=ivi`` - forces usage of National Instruments Visa
			- ``QueryInstrumentStatus = False`` - same as ``driver.utilities.instrument_status_checking = False``. Default: ``True``
			- ``WriteDelay = 20, ReadDelay = 5`` - Introduces delay of 20ms before each write and 5ms before each read. Default: ``0ms`` for both
			- ``OpcWaitMode = OpcQuery`` - mode for all the opc-synchronised write/reads. Other modes: StbPolling, StbPollingSlow, StbPollingSuperSlow. Default: ``StbPolling``
			- ``AddTermCharToWriteBinBLock = True`` - Adds one additional LF to the end of the binary data (some instruments require that). Default: ``False``
			- ``AssureWriteWithTermChar = True`` - Makes sure each command/query is terminated with termination character. Default: Interface dependent
			- ``TerminationCharacter = "\\r"`` - Sets the termination character for reading. Default: ``\\n`` (LineFeed or LF)
			- ``DataChunkSize = 10E3`` - Maximum size of one write/read segment. If transferred data is bigger, it is split to more segments. Default: ``1E6`` bytes
			- ``OpcTimeout = 10000`` - same as driver.utilities.opc_timeout = 10000. Default: ``30000ms``
			- ``VisaTimeout = 5000`` - same as driver.utilities.visa_timeout = 5000. Default: ``10000ms``
			- ``ViClearExeMode = Disabled`` - viClear() execution mode. Default: ``execute_on_all``
			- ``OpcQueryAfterWrite = True`` - same as driver.utilities.opc_query_after_write = True. Default: ``False``
			- ``StbInErrorCheck = False`` - if true, the driver checks errors with *STB? If false, it uses SYST:ERR?. Default: ``True``
			- ``LoggingMode = LoggingMode.On`` - Sets the logging status right from the start. Default: ``Off``
			- ``LoggingName = 'MyDevice'`` - Sets the name to represent the session in the log entries. Default: ``'resource_name'``
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception.
		:param reset: Resets the instrument (sends *RST command) and clears its status sybsystem
		:param options: string tokens alternating the driver settings.
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session."""
		self._core = Core(resource_name, id_query, reset, RsNgx._driver_options, options, direct_session)
		self._core.driver_version = '3.1.0.0048'
		self._options = options
		self._add_all_global_repcaps()
		self._custom_properties_init()
		# noinspection PyTypeChecker
		self._base = CommandsGroup("ROOT", self._core, None)
		self._selected_channel = int(self._core.io.query_str('INSTrument:NSELect?', True))
		self._persistent_channel: int = 0

		def _before_write_callback(io, cmd: str) -> None:
			"""Callback that assures the INSTrument:NSELect value is persistent before every write command."""
			if self._persistent_channel == 0:
				return
			sent = cmd.split(' ')
			if sent[0] == 'INSTrument:NSELect':
				# We actually want to change the channel, can not do this with the persistence ON
				raise RsInstrException(f'You can not use the rsnrx.instrument.select.set() while the channel persistence is switched ON to channel {self._persistent_channel}.')
			if sent[0].startswith('APPLy'):
				# Exceptions for commands that do not need channel selection
				return
			self._assure_channel_selected(io)

		def _before_query_callback(io, cmd: str) -> None:
			"""Callback that assures the INSTrument:NSELect value is persistent before every query."""
			if self._persistent_channel == 0:
				return
			if cmd == 'INSTrument:NSELect?':
				# Exceptions for commands that do not need channel selection
				return
			self._assure_channel_selected(io)

		self._core.io.before_write_handler = _before_write_callback
		self._core.io.before_query_handler = _before_query_callback

	def set_persistent_channel(self, channel: int) -> None:
		"""If set to 0 (default value), the driver behaves exactly as the SCPI interface - you can select the addressed channel with rsnrx.instrument.select.set().
		If you set this property to 1 .. 8 (depending on how many channels your device has), the drivers makes sure that for each function you call,
		this channel is preselected, no matter which channel is currently active. In this mode you can not use the rsnrx.instrument.select.set()"""
		self._persistent_channel = channel
		if channel == 0:
			# For channel 0, do not do anything else
			return
		# Set the channel and make sure it will be persistent further on...
		self._core.io.write(f'INSTrument:NSELect {channel}', True)
		self._selected_channel = channel

	def get_persistent_channel(self) -> int:
		"""Returns the current persistent channel. If the persistence is switched off, the method returns 0."""
		return self._persistent_channel

	def _assure_channel_selected(self, io):
		# Make sure the persistent channel is selected
		status_check = io.query_instr_status
		try:
			io.query_instr_status = False
			channel = int(io.query_str('INSTrument:NSELect?', True))
			if channel != self._selected_channel:
				io.write(f'INSTrument:NSELect {self._selected_channel}', True)
		finally:
			io.query_instr_status = status_check

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsNgx':
		"""Creates a new RsNgx object with the entered 'session' reused. \n
		:param session: can be an another driver or a direct pyvisa session.
		:param options: string tokens alternating the driver settings."""
		# noinspection PyTypeChecker
		return cls(None, False, False, options, session)

	def __str__(self) -> str:
		if self._core.io:
			return f"RsNgx session '{self._core.io.resource_name}'"
		else:
			return f"RsNgx with session closed"

	@staticmethod
	def assert_minimum_version(min_version: str) -> None:
		"""Asserts that the driver version fulfills the minimum required version you have entered.
		This way you make sure your installed driver is of the entered version or newer."""
		min_version_list = min_version.split('.')
		curr_version_list = '3.1.0.0048'.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise RsInstrException(f"Assertion for minimum RsNgx version failed. Current version: '3.1.0.0048', minimum required version: '{min_version}'")
				
	@staticmethod
	def list_resources(expression: str = '?*::INSTR', visa_select: str = None) -> List[str]:
		"""Finds all the resources defined by the expression
			- '?*' - matches all the available instruments
			- 'USB::?*' - matches all the USB instruments
			- "TCPIP::192?*' - matches all the LAN instruments with the IP address starting with 192
		:param expression: see the examples in the function
		:param visa_select: optional parameter selecting a specific VISA. Examples: '@ivi', '@rs'
		"""
		rm = VisaSession.get_resource_manager(visa_select)
		resources = rm.list_resources(expression)
		rm.close()
		# noinspection PyTypeChecker
		return resources

	def close(self) -> None:
		"""Closes the active RsNgx session."""
		self._core.io.close()

	def get_session_handle(self) -> object:
		"""Returns the underlying session handle."""
		return self._core.get_session_handle()

	def _add_all_global_repcaps(self) -> None:
		"""Adds all the repcaps defined as global to the instrument's global repcaps dictionary."""

	def _custom_properties_init(self):
		"""Adds all the interfaces that are custom for the driver."""
		from .CustomFiles.utilities import Utilities
		self.utilities = Utilities(self._core)
		from .CustomFiles.events import Events
		self.events = Events(self._core)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Implementations.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def arbitrary(self):
		"""arbitrary commands group. 6 Sub-classes, 7 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Implementations.Arbitrary import Arbitrary
			self._arbitrary = Arbitrary(self._core, self._base)
		return self._arbitrary

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Implementations.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def fuse(self):
		"""fuse commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_fuse'):
			from .Implementations.Fuse import Fuse
			self._fuse = Fuse(self._core, self._base)
		return self._fuse

	@property
	def instrument(self):
		"""instrument commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_instrument'):
			from .Implementations.Instrument import Instrument
			self._instrument = Instrument(self._core, self._base)
		return self._instrument

	@property
	def tracking(self):
		"""tracking commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tracking'):
			from .Implementations.Tracking import Tracking
			self._tracking = Tracking(self._core, self._base)
		return self._tracking

	@property
	def calibration(self):
		"""calibration commands group. 7 Sub-classes, 7 commands."""
		if not hasattr(self, '_calibration'):
			from .Implementations.Calibration import Calibration
			self._calibration = Calibration(self._core, self._base)
		return self._calibration

	@property
	def log(self):
		"""log commands group. 8 Sub-classes, 3 commands."""
		if not hasattr(self, '_log'):
			from .Implementations.Log import Log
			self._log = Log(self._core, self._base)
		return self._log

	@property
	def measure(self):
		"""measure commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_measure'):
			from .Implementations.Measure import Measure
			self._measure = Measure(self._core, self._base)
		return self._measure

	@property
	def output(self):
		"""output commands group. 6 Sub-classes, 3 commands."""
		if not hasattr(self, '_output'):
			from .Implementations.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def system(self):
		"""system commands group. 10 Sub-classes, 3 commands."""
		if not hasattr(self, '_system'):
			from .Implementations.System import System
			self._system = System(self._core, self._base)
		return self._system

	@property
	def source(self):
		"""source commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_source'):
			from .Implementations.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def status(self):
		"""status commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_status'):
			from .Implementations.Status import Status
			self._status = Status(self._core, self._base)
		return self._status

	@property
	def trigger(self):
		"""trigger commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Implementations.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def sense(self):
		"""sense commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sense'):
			from .Implementations.Sense import Sense
			self._sense = Sense(self._core, self._base)
		return self._sense

	@property
	def dio(self):
		"""dio commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dio'):
			from .Implementations.Dio import Dio
			self._dio = Dio(self._core, self._base)
		return self._dio

	@property
	def flog(self):
		"""flog commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_flog'):
			from .Implementations.Flog import Flog
			self._flog = Flog(self._core, self._base)
		return self._flog

	@property
	def battery(self):
		"""battery commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_battery'):
			from .Implementations.Battery import Battery
			self._battery = Battery(self._core, self._base)
		return self._battery

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Implementations.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def hardCopy(self):
		"""hardCopy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_hardCopy'):
			from .Implementations.HardCopy import HardCopy
			self._hardCopy = HardCopy(self._core, self._base)
		return self._hardCopy

	@property
	def interfaces(self):
		"""interfaces commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_interfaces'):
			from .Implementations.Interfaces import Interfaces
			self._interfaces = Interfaces(self._core, self._base)
		return self._interfaces

	# noinspection PyTypeChecker
	class Measurement(StructBase):
		"""Response structure. Fields: \n
			- Voltage: float: No parameter help available
			- Current: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Voltage'),
			ArgStruct.scalar_float('Current')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Voltage: float = None
			self.Current: float = None

	def read(self) -> Measurement:
		"""SCPI: READ \n
		Snippet: value: Measurement = driver.read() \n
		Queries for the next available readback for voltage and current of the selected channel. \n
			:return: structure: for return value, see the help for Measurement structure arguments."""
		return self._core.io.query_struct_with_opc(f'READ?', self.__class__.Measurement())

	def clone(self) -> 'RsNgx':
		"""Creates a deep copy of the RsNgx object.
		After cloning, your new RsNgx object can be used separately, but shares the same instrument session.
		Calling close() on the new object does not close the original VISA session.
		This method is similar to calling RsNgx.from_existing_session()"""
		cloned = RsNgx.from_existing_session(self.get_session_handle(), self._options)
		self._base.synchronize_repcaps(cloned)
		
		return cloned
