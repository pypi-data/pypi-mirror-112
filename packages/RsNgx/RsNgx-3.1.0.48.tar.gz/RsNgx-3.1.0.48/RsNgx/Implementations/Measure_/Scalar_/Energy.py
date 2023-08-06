from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Energy:
	"""Energy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("energy", core, parent)

	def get_state(self) -> bool:
		"""SCPI: MEASure[:SCALar]:ENERgy:STATe \n
		Snippet: value: bool = driver.measure.scalar.energy.get_state() \n
		Sets or queries the energy counter state for the selected channel. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:ENERgy:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arg_0: bool) -> None:
		"""SCPI: MEASure[:SCALar]:ENERgy:STATe \n
		Snippet: driver.measure.scalar.energy.set_state(arg_0 = False) \n
		Sets or queries the energy counter state for the selected channel. \n
			:param arg_0:
				- 1: Activates the energy counter.
				- 0: Deactivates the energy counter."""
		param = Conversions.bool_to_str(arg_0)
		self._core.io.write(f'MEASure:SCALar:ENERgy:STATe {param}')

	def reset(self) -> None:
		"""SCPI: MEASure[:SCALar]:ENERgy:RESet \n
		Snippet: driver.measure.scalar.energy.reset() \n
		Resets the energy counter for the selected channel. \n
		"""
		self._core.io.write(f'MEASure:SCALar:ENERgy:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: MEASure[:SCALar]:ENERgy:RESet \n
		Snippet: driver.measure.scalar.energy.reset_with_opc() \n
		Resets the energy counter for the selected channel. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'MEASure:SCALar:ENERgy:RESet')

	def get_value(self) -> float:
		"""SCPI: MEASure[:SCALar]:ENERgy \n
		Snippet: value: float = driver.measure.scalar.energy.get_value() \n
		Queries the measured the current released energy value of the previous selected channel. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('MEASure:SCALar:ENERgy?')
		return Conversions.str_to_float(response)
