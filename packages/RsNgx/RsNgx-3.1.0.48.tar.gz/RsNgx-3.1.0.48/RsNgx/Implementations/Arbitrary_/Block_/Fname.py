from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fname:
	"""Fname commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fname", core, parent)

	def set(self, arg_0: str, arg_1: enums.Filename = None) -> None:
		"""SCPI: ARBitrary:BLOCk:FNAMe \n
		Snippet: driver.arbitrary.block.fname.set(arg_0 = '1', arg_1 = enums.Filename.DEF) \n
		Sets or queries the filename for block of arbitrary data. \n
			:param arg_0: No help available
			:param arg_1: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.String), ArgSingle('arg_1', arg_1, DataType.Enum, True))
		self._core.io.write(f'ARBitrary:BLOCk:FNAMe {param}'.rstrip())

	def get(self, arg_0: str, arg_1: enums.Filename = None) -> str:
		"""SCPI: ARBitrary:BLOCk:FNAMe \n
		Snippet: value: str = driver.arbitrary.block.fname.get(arg_0 = '1', arg_1 = enums.Filename.DEF) \n
		Sets or queries the filename for block of arbitrary data. \n
			:param arg_0: No help available
			:param arg_1: No help available
			:return: arg_0: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('arg_0', arg_0, DataType.String), ArgSingle('arg_1', arg_1, DataType.Enum, True))
		response = self._core.io.query_str(f'ARBitrary:BLOCk:FNAMe? {param}'.rstrip())
		return trim_str_response(response)
