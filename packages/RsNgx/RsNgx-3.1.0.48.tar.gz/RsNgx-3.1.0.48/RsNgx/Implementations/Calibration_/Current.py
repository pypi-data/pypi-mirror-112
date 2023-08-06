from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def imin(self):
		"""imin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imin'):
			from .Current_.Imin import Imin
			self._imin = Imin(self._core, self._base)
		return self._imin

	@property
	def imax(self):
		"""imax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imax'):
			from .Current_.Imax import Imax
			self._imax = Imax(self._core, self._base)
		return self._imax

	def get_data(self) -> float:
		"""SCPI: CALibration:CURRent:DATA \n
		Snippet: value: float = driver.calibration.current.get_data() \n
		Set the DMM reading after setting the output current level in channel adjustment process. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('CALibration:CURRent:DATA?')
		return Conversions.str_to_float(response)

	def set_data(self, arg_0: float) -> None:
		"""SCPI: CALibration:CURRent:DATA \n
		Snippet: driver.calibration.current.set_data(arg_0 = 1.0) \n
		Set the DMM reading after setting the output current level in channel adjustment process. \n
			:param arg_0: Measured value from DMM.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'CALibration:CURRent:DATA {param}')
