from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, format_py: enums.HcpyFormat) -> None:
		"""SCPI: HCOPy:FORMat \n
		Snippet: driver.hardCopy.formatPy.set(format_py = enums.HcpyFormat.BMP) \n
		No command help available \n
			:param format_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.HcpyFormat)
		self._core.io.write(f'HCOPy:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, format_py: enums.HcpyFormat) -> enums.HcpyFormat:
		"""SCPI: HCOPy:FORMat \n
		Snippet: value: enums.HcpyFormat = driver.hardCopy.formatPy.get(format_py = enums.HcpyFormat.BMP) \n
		No command help available \n
			:param format_py: No help available
			:return: format_py: No help available"""
		param = Conversions.enum_scalar_to_str(format_py, enums.HcpyFormat)
		response = self._core.io.query_str(f'HCOPy:FORMat? {param}')
		return Conversions.str_to_scalar_enum(response, enums.HcpyFormat)
