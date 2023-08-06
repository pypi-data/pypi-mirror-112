from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def get_capacitance(self) -> str:
		"""SCPI: OUTPut:MODE:CAPacitance \n
		Snippet: value: str = driver.output.mode.get_capacitance() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str_with_opc('OUTPut:MODE:CAPacitance?')
		return trim_str_response(response)

	def set_capacitance(self, arg_0: str) -> None:
		"""SCPI: OUTPut:MODE:CAPacitance \n
		Snippet: driver.output.mode.set_capacitance(arg_0 = r1) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:MODE:CAPacitance {param}')

	def get_value(self) -> str:
		"""SCPI: OUTPut:MODE \n
		Snippet: value: str = driver.output.mode.get_value() \n
		Sets or queries the output mode. \n
			:return: arg_0: AUTO | SINK | SOURce | list AUTO If operates in auto mode, the R&S NGU goes into sink or source mode depending on the voltage across the output terminal. If voltage across the output terminal exceeds the set voltage, current flows into the instrument, e.g. the instrument is now operating in sink mode; vv if voltage across output terminal is below set voltage, instrument operates as a source mode. SINK If operates in sink mode, current flows into the instrument. On display, current is shown as negative current. SOURce If operates in source mode, current flows out from the instrument.
		"""
		response = self._core.io.query_str_with_opc('OUTPut:MODE?')
		return trim_str_response(response)

	def set_value(self, arg_0: str) -> None:
		"""SCPI: OUTPut:MODE \n
		Snippet: driver.output.mode.set_value(arg_0 = r1) \n
		Sets or queries the output mode. \n
			:param arg_0: AUTO | SINK | SOURce | list AUTO If operates in auto mode, the R&S NGU goes into sink or source mode depending on the voltage across the output terminal. If voltage across the output terminal exceeds the set voltage, current flows into the instrument, e.g. the instrument is now operating in sink mode; vv if voltage across output terminal is below set voltage, instrument operates as a source mode. SINK If operates in sink mode, current flows into the instrument. On display, current is shown as negative current. SOURce If operates in source mode, current flows out from the instrument.
		"""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:MODE {param}')
