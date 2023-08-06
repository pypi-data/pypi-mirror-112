from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ainput:
	"""Ainput commands group definition. 9 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ainput", core, parent)

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Ainput_.Start import Start
			self._start = Start(self._core, self._base)
		return self._start

	@property
	def cancel(self):
		"""cancel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cancel'):
			from .Ainput_.Cancel import Cancel
			self._cancel = Cancel(self._core, self._base)
		return self._cancel

	@property
	def end(self):
		"""end commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_end'):
			from .Ainput_.End import End
			self._end = End(self._core, self._base)
		return self._end

	@property
	def umin(self):
		"""umin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umin'):
			from .Ainput_.Umin import Umin
			self._umin = Umin(self._core, self._base)
		return self._umin

	@property
	def umax(self):
		"""umax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umax'):
			from .Ainput_.Umax import Umax
			self._umax = Umax(self._core, self._base)
		return self._umax

	def save(self) -> None:
		"""SCPI: CALibration:AINPut:SAVE \n
		Snippet: driver.calibration.ainput.save() \n
		Saves the analog input adjustment. \n
		"""
		self._core.io.write(f'CALibration:AINPut:SAVE')

	def save_with_opc(self) -> None:
		"""SCPI: CALibration:AINPut:SAVE \n
		Snippet: driver.calibration.ainput.save_with_opc() \n
		Saves the analog input adjustment. \n
		Same as save, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:AINPut:SAVE')

	def get_data(self) -> float:
		"""SCPI: CALibration:AINPut:DATA \n
		Snippet: value: float = driver.calibration.ainput.get_data() \n
		Sets the analog input adjustment data. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('CALibration:AINPut:DATA?')
		return Conversions.str_to_float(response)

	def set_data(self, arg_0: float) -> None:
		"""SCPI: CALibration:AINPut:DATA \n
		Snippet: driver.calibration.ainput.set_data(arg_0 = 1.0) \n
		Sets the analog input adjustment data. \n
			:param arg_0: Measured value from DMM.
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'CALibration:AINPut:DATA {param}')

	def get_date(self) -> str:
		"""SCPI: CALibration:AINPut:DATE \n
		Snippet: value: str = driver.calibration.ainput.get_date() \n
		Returns the analog input adjustment date ('DD-MM-YY') . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('CALibration:AINPut:DATE?')
		return trim_str_response(response)

	def get_count(self) -> int:
		"""SCPI: CALibration:AINPut:COUNt \n
		Snippet: value: int = driver.calibration.ainput.get_count() \n
		Queries the number of counts performed for analog input adjustment . \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('CALibration:AINPut:COUNt?')
		return Conversions.str_to_int(response)
