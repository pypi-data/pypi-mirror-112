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
		"""SCPI: STATus:OPERation:INSTrument[:EVENt] \n
		Snippet: value: int = driver.status.operation.instrument.get_event() \n
		Returns the contents of the EVENt part of the status register to check whether an event has occurred since the last
		reading. Reading an EVENt register deletes its contents. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('STATus:OPERation:INSTrument:EVENt?')
		return Conversions.str_to_int(response)

	def get_condition(self) -> int:
		"""SCPI: STATus:OPERation:INSTrument:CONDition \n
		Snippet: value: int = driver.status.operation.instrument.get_condition() \n
		Returns the contents of the CONDition part of the status register to check for operation instrument or measurement states.
		Reading the CONDition registers does not delete the contents. \n
			:return: result: Condition bits in decimal representation.
		"""
		response = self._core.io.query_str('STATus:OPERation:INSTrument:CONDition?')
		return Conversions.str_to_int(response)

	def get_ptransition(self) -> int:
		"""SCPI: STATus:OPERation:INSTrument:PTRansition \n
		Snippet: value: int = driver.status.operation.instrument.get_ptransition() \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:OPERation:INSTrument:PTRansition?')
		return Conversions.str_to_int(response)

	def set_ptransition(self, arg_0: int) -> None:
		"""SCPI: STATus:OPERation:INSTrument:PTRansition \n
		Snippet: driver.status.operation.instrument.set_ptransition(arg_0 = 1) \n
		Sets or queries the positive transition filter. Setting a bit in the positive transition filter shall cause a 0 to 1
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:OPERation:INSTrument:PTRansition {param}')

	def get_ntransition(self) -> int:
		"""SCPI: STATus:OPERation:INSTrument:NTRansition \n
		Snippet: value: int = driver.status.operation.instrument.get_ntransition() \n
		Sets or queries the negative transition filter. Setting a bit in the negative transition filter shall cause a 1 to 0
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:OPERation:INSTrument:NTRansition?')
		return Conversions.str_to_int(response)

	def set_ntransition(self, arg_0: int) -> None:
		"""SCPI: STATus:OPERation:INSTrument:NTRansition \n
		Snippet: driver.status.operation.instrument.set_ntransition(arg_0 = 1) \n
		Sets or queries the negative transition filter. Setting a bit in the negative transition filter shall cause a 1 to 0
		transition in the corresponding bit of the associated condition register to cause a 1 to be written in the associated bit
		of the corresponding event register. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:OPERation:INSTrument:NTRansition {param}')

	def get_enable(self) -> int:
		"""SCPI: STATus:OPERation:INSTrument:ENABle \n
		Snippet: value: int = driver.status.operation.instrument.get_enable() \n
		Controls or queries the ENABle part of the STATus:OPERation register. The ENABle defines which events in the EVENt part
		of the status register are forwarded to the OPERation summary bit (bit 7) of the status byte. The status byte can be used
		to create a service request. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('STATus:OPERation:INSTrument:ENABle?')
		return Conversions.str_to_int(response)

	def set_enable(self, arg_0: int) -> None:
		"""SCPI: STATus:OPERation:INSTrument:ENABle \n
		Snippet: driver.status.operation.instrument.set_enable(arg_0 = 1) \n
		Controls or queries the ENABle part of the STATus:OPERation register. The ENABle defines which events in the EVENt part
		of the status register are forwarded to the OPERation summary bit (bit 7) of the status byte. The status byte can be used
		to create a service request. \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'STATus:OPERation:INSTrument:ENABle {param}')
