from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.Utilities import trim_str_response
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class System:
	"""System commands group definition. 46 total commands, 10 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("system", core, parent)

	@property
	def beeper(self):
		"""beeper commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_beeper'):
			from .System_.Beeper import Beeper
			self._beeper = Beeper(self._core, self._base)
		return self._beeper

	@property
	def touch(self):
		"""touch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_touch'):
			from .System_.Touch import Touch
			self._touch = Touch(self._core, self._base)
		return self._touch

	@property
	def communicate(self):
		"""communicate commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_communicate'):
			from .System_.Communicate import Communicate
			self._communicate = Communicate(self._core, self._base)
		return self._communicate

	@property
	def key(self):
		"""key commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_key'):
			from .System_.Key import Key
			self._key = Key(self._core, self._base)
		return self._key

	@property
	def local(self):
		"""local commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_local'):
			from .System_.Local import Local
			self._local = Local(self._core, self._base)
		return self._local

	@property
	def remote(self):
		"""remote commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_remote'):
			from .System_.Remote import Remote
			self._remote = Remote(self._core, self._base)
		return self._remote

	@property
	def rwLock(self):
		"""rwLock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rwLock'):
			from .System_.RwLock import RwLock
			self._rwLock = RwLock(self._core, self._base)
		return self._rwLock

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .System_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_setting'):
			from .System_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def vnc(self):
		"""vnc commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vnc'):
			from .System_.Vnc import Vnc
			self._vnc = Vnc(self._core, self._base)
		return self._vnc

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Year: float: Sets year of the date.
			- Month: float: Sets month of the date.
			- Day: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Year'),
			ArgStruct.scalar_float('Month'),
			ArgStruct.scalar_float('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: float = None
			self.Month: float = None
			self.Day: float = None

	def get_date(self) -> DateStruct:
		"""SCPI: SYSTem:DATE \n
		Snippet: value: DateStruct = driver.system.get_date() \n
		Sets or queries the system date. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:DATE?', self.__class__.DateStruct())

	def set_date(self, value: DateStruct) -> None:
		"""SCPI: SYSTem:DATE \n
		Snippet: driver.system.set_date(value = DateStruct()) \n
		Sets or queries the system date. \n
			:param value: see the help for DateStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:DATE', value)

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: No parameter help available
			- Minute: int: No parameter help available
			- Second: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_int('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: int = None

	def get_time(self) -> TimeStruct:
		"""SCPI: SYSTem:TIME \n
		Snippet: value: TimeStruct = driver.system.get_time() \n
		Sets or queries the system time. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:TIME?', self.__class__.TimeStruct())

	def set_time(self, value: TimeStruct) -> None:
		"""SCPI: SYSTem:TIME \n
		Snippet: driver.system.set_time(value = TimeStruct()) \n
		Sets or queries the system time. \n
			:param value: see the help for TimeStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:TIME', value)

	def get_up_time(self) -> str:
		"""SCPI: SYSTem:UPTime \n
		Snippet: value: str = driver.system.get_up_time() \n
		Queries system uptime. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('SYSTem:UPTime?')
		return trim_str_response(response)
