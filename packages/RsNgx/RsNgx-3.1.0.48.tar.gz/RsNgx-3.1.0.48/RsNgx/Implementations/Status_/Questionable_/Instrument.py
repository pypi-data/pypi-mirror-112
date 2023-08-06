from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Instrument:
	"""Instrument commands group definition. 10 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("instrument", core, parent)

	@property
	def isummary(self):
		"""isummary commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_isummary'):
			from .Instrument_.Isummary import Isummary
			self._isummary = Isummary(self._core, self._base)
		return self._isummary

	def get_event(self) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument[:EVENt] \n
		Snippet: value: int = driver.status.questionable.instrument.get_event() \n
		Returns the contents of the EVENt part of the status register to check whether an event has occurred since the last
		reading. Reading an EVENt register deletes its contents. \n
			:return: result: Event bits in decimal representation
		"""
		response = self._core.io.query_str('STATus:QUEStionable:INSTrument:EVENt?')
		return Conversions.str_to_int(response)

	def get_condition(self) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:CONDition \n
		Snippet: value: int = driver.status.questionable.instrument.get_condition() \n
		Returns the contents of the CONDition part of the status register to check for questionable instrument or measurement
		states. Reading the CONDition registers does not delete the contents. \n
			:return: result: Condition bits in decimal representation
		"""
		response = self._core.io.query_str('STATus:QUEStionable:INSTrument:CONDition?')
		return Conversions.str_to_int(response)

	def get_ptransition(self) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:PTRansition \n
		Snippet: value: int = driver.status.questionable.instrument.get_ptransition() \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:INSTrument:PTRansition?')
		return Conversions.str_to_int(response)

	def set_ptransition(self, arg_0: int) -> None:
		"""SCPI: STATus:QUEStionable:INSTrument:PTRansition \n
		Snippet: driver.status.questionable.instrument.set_ptransition(arg_0 = 1) \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:QUEStionable:INSTrument:PTRansition {param}')

	def get_ntransition(self) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:NTRansition \n
		Snippet: value: int = driver.status.questionable.instrument.get_ntransition() \n
		Sets or queries the negative transition filter. Setting a bit in the negative transition filter shall cause a 1 to 0
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:INSTrument:NTRansition?')
		return Conversions.str_to_int(response)

	def set_ntransition(self, arg_0: int) -> None:
		"""SCPI: STATus:QUEStionable:INSTrument:NTRansition \n
		Snippet: driver.status.questionable.instrument.set_ntransition(arg_0 = 1) \n
		Sets or queries the negative transition filter. Setting a bit in the negative transition filter shall cause a 1 to 0
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:QUEStionable:INSTrument:NTRansition {param}')

	def get_enable(self) -> int:
		"""SCPI: STATus:QUEStionable:INSTrument:ENABle \n
		Snippet: value: int = driver.status.questionable.instrument.get_enable() \n
		Sets or queries the enable mask that allows true conditions in the EVENt part to be reported in the summary bit. If a bit
		in the ENABle part is 1, and the corresponding EVENt bit is true, a positive transition occurs in the summary bit. This
		transition is reported to the next higher level. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:INSTrument:ENABle?')
		return Conversions.str_to_int(response)

	def set_enable(self, arg_0: int) -> None:
		"""SCPI: STATus:QUEStionable:INSTrument:ENABle \n
		Snippet: driver.status.questionable.instrument.set_enable(arg_0 = 1) \n
		Sets or queries the enable mask that allows true conditions in the EVENt part to be reported in the summary bit. If a bit
		in the ENABle part is 1, and the corresponding EVENt bit is true, a positive transition occurs in the summary bit. This
		transition is reported to the next higher level. \n
			:param arg_0: Bit mask in decimal representation
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:QUEStionable:INSTrument:ENABle {param}')
