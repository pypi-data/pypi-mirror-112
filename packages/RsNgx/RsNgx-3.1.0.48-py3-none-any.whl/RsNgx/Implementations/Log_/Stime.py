from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stime:
	"""Stime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stime", core, parent)

	# noinspection PyTypeChecker
	class SetStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Year: int: No parameter help available
			- Month: int: No parameter help available
			- Day: int: No parameter help available
			- Hour: int: No parameter help available
			- Minute: int: No parameter help available
			- Second: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None
			self.Hour: int = None
			self.Minute: int = None
			self.Second: int = None

	def set(self, structure: SetStruct) -> None:
		"""SCPI: LOG:STIMe \n
		Snippet: driver.log.stime.set(value = [PROPERTY_STRUCT_NAME]()) \n
		Sets or queries the start time of the data logging function. \n
			:param structure: for set value, see the help for SetStruct structure arguments.
		"""
		self._core.io.write_struct(f'LOG:STIMe', structure)

	def get(self) -> str:
		"""SCPI: LOG:STIMe \n
		Snippet: value: str = driver.log.stime.get() \n
		Sets or queries the start time of the data logging function. \n
			:return: result: No help available"""
		response = self._core.io.query_str(f'LOG:STIMe?')
		return trim_str_response(response)
