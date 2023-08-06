from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("start", core, parent)

	def set(self, arg_0: int) -> None:
		"""SCPI: CALibration:AINPut:STARt \n
		Snippet: driver.calibration.ainput.start.set(arg_0 = 1) \n
		Selects the analog input pin for adjustment. \n
			:param arg_0: Input pin for adjustment.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'CALibration:AINPut:STARt {param}')

	def get(self) -> int:
		"""SCPI: CALibration:AINPut:STARt \n
		Snippet: value: int = driver.calibration.ainput.start.get() \n
		Selects the analog input pin for adjustment. \n
			:return: arg_0: No help available"""
		response = self._core.io.query_str(f'CALibration:AINPut:STARt?')
		return Conversions.str_to_int(response)
