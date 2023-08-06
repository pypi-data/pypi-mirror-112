from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voltage:
	"""Voltage commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voltage", core, parent)

	@property
	def umin(self):
		"""umin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umin'):
			from .Voltage_.Umin import Umin
			self._umin = Umin(self._core, self._base)
		return self._umin

	@property
	def umax(self):
		"""umax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umax'):
			from .Voltage_.Umax import Umax
			self._umax = Umax(self._core, self._base)
		return self._umax

	def get_data(self) -> float:
		"""SCPI: CALibration:VOLTage:DATA \n
		Snippet: value: float = driver.calibration.voltage.get_data() \n
		Sets the DMM reading after setting the output voltage level in channel adjustment process. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('CALibration:VOLTage:DATA?')
		return Conversions.str_to_float(response)

	def set_data(self, arg_0: float) -> None:
		"""SCPI: CALibration:VOLTage:DATA \n
		Snippet: driver.calibration.voltage.set_data(arg_0 = 1.0) \n
		Sets the DMM reading after setting the output voltage level in channel adjustment process. \n
			:param arg_0: Measured value from DMM.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'CALibration:VOLTage:DATA {param}')
