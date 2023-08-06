from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def get_tpartition(self) -> str:
		"""SCPI: FLOG:FILE:TPARtition \n
		Snippet: value: str = driver.flog.file.get_tpartition() \n
		Selects the external partition to which the data is written into. \n
			:return: arg_0: Defines the external path partition to which the data is written in the USB stick.
		"""
		response = self._core.io.query_str('FLOG:FILE:TPARtition?')
		return trim_str_response(response)

	def set_tpartition(self, arg_0: str) -> None:
		"""SCPI: FLOG:FILE:TPARtition \n
		Snippet: driver.flog.file.set_tpartition(arg_0 = '1') \n
		Selects the external partition to which the data is written into. \n
			:param arg_0: Defines the external path partition to which the data is written in the USB stick.
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'FLOG:FILE:TPARtition {param}')

	def get_duration(self) -> float:
		"""SCPI: FLOG:FILE:DURation \n
		Snippet: value: float = driver.flog.file.get_duration() \n
		Sets or queries the file write duration. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('FLOG:FILE:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, arg_0: float) -> None:
		"""SCPI: FLOG:FILE:DURation \n
		Snippet: driver.flog.file.set_duration(arg_0 = 1.0) \n
		Sets or queries the file write duration. \n
			:param arg_0: Sets file write duration.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'FLOG:FILE:DURation {param}')
