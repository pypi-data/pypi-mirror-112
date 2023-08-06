from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Location:
	"""Location commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("location", core, parent)

	def set(self, arg_0: enums.Filename = None) -> None:
		"""SCPI: LOG:LOCation \n
		Snippet: driver.log.location.set(arg_0 = enums.Filename.DEF) \n
		Sets or queries the logging location. \n
			:param arg_0: No help available
		"""
		param = ''
		if arg_0:
			param = Conversions.enum_scalar_to_str(arg_0, enums.Filename)
		self._core.io.write(f'LOG:LOCation {param}'.strip())

	# noinspection PyTypeChecker
	def get(self, arg_0: enums.Filename = None) -> enums.Filename:
		"""SCPI: LOG:LOCation \n
		Snippet: value: enums.Filename = driver.log.location.get(arg_0 = enums.Filename.DEF) \n
		Sets or queries the logging location. \n
			:param arg_0: No help available
			:return: arg_0: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.Enum, True))
		response = self._core.io.query_str(f'LOG:LOCation? {param}'.rstrip())
		return Conversions.str_to_scalar_enum(response, enums.Filename)
