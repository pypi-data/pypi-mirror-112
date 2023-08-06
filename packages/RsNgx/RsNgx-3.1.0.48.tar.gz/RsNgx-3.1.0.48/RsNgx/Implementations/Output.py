from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 13 total commands, 6 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	@property
	def general(self):
		"""general commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_general'):
			from .Output_.General import General
			self._general = General(self._core, self._base)
		return self._general

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Output_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_impedance'):
			from .Output_.Impedance import Impedance
			self._impedance = Impedance(self._core, self._base)
		return self._impedance

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Output_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def triggered(self):
		"""triggered commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_triggered'):
			from .Output_.Triggered import Triggered
			self._triggered = Triggered(self._core, self._base)
		return self._triggered

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Output_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	def get_state(self) -> bool:
		"""SCPI: OUTPut[:STATe] \n
		Snippet: value: bool = driver.output.get_state() \n
		Sets or queries the output state of the previous selected channels. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: OUTPut[:STATe] \n
		Snippet: driver.output.set_state(arg_0 = False) \n
		Sets or queries the output state of the previous selected channels. \n
			:param arg_0:
				- 0: Switches off previous selected channels.
				- 1: Switches on previous selected channels."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:STATe {param}')

	def get_select(self) -> bool:
		"""SCPI: OUTPut:SELect \n
		Snippet: value: bool = driver.output.get_select() \n
		Sets or queries the output state of selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:SELect?')
		return Conversions.str_to_bool(response)

	def set_select(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:SELect \n
		Snippet: driver.output.set_select(arg_0 = False) \n
		Sets or queries the output state of selected channel. \n
			:param arg_0:
				- 0: Deactivates the selected channel.
				- 1: Activates the selected channel."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:SELect {param}')

	def get_ft_response(self) -> bool:
		"""SCPI: OUTPut:FTResponse \n
		Snippet: value: bool = driver.output.get_ft_response() \n
		Sets or queries the fast transient response state. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:FTResponse?')
		return Conversions.str_to_bool(response)

	def set_ft_response(self, arg_0: bool) -> None:
		"""SCPI: OUTPut:FTResponse \n
		Snippet: driver.output.set_ft_response(arg_0 = False) \n
		Sets or queries the fast transient response state. \n
			:param arg_0: No help available
		"""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:FTResponse {param}')
