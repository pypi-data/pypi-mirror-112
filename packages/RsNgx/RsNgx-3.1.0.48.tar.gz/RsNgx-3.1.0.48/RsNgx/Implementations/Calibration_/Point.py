from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Point:
	"""Point commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("point", core, parent)

	def set(self, arg_0: int) -> None:
		"""SCPI: CALibration:POINt \n
		Snippet: driver.calibration.point.set(arg_0 = 1) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'CALibration:POINt {param}')

	def get(self, arg_0: int) -> int:
		"""SCPI: CALibration:POINt \n
		Snippet: value: int = driver.calibration.point.get(arg_0 = 1) \n
		No command help available \n
			:param arg_0: No help available
			:return: arg_0: No help available"""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str(f'CALibration:POINt? {param}')
		return Conversions.str_to_int(response)
