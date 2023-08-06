from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, arg_0: enums.LogMode) -> None:
		"""SCPI: LOG:MODE \n
		Snippet: driver.log.mode.set(arg_0 = enums.LogMode.COUNt) \n
		Sets or queries the data logging mode. \n
			:param arg_0:
				- UNLimited: Infinite data capture.
				- COUNt: Number of measurement values to be captured.
				- DURation: Duration of the measurement values capture.
				- SPAN: Interval of the measurement values capture."""
		param = Conversions.enum_scalar_to_str(arg_0, enums.LogMode)
		self._core.io.write(f'LOG:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, arg_0: enums.LogMode) -> enums.LogMode:
		"""SCPI: LOG:MODE \n
		Snippet: value: enums.LogMode = driver.log.mode.get(arg_0 = enums.LogMode.COUNt) \n
		Sets or queries the data logging mode. \n
			:param arg_0:
				- UNLimited: Infinite data capture.
				- COUNt: Number of measurement values to be captured.
				- DURation: Duration of the measurement values capture.
				- SPAN: Interval of the measurement values capture.
			:return: arg_0: No help available"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.LogMode)
		response = self._core.io.query_str(f'LOG:MODE? {param}')
		return Conversions.str_to_scalar_enum(response, enums.LogMode)
