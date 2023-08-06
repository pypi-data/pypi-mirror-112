from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sense:
	"""Sense commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sense", core, parent)

	def get_source(self) -> str:
		"""SCPI: [SOURce]:VOLTage:SENSe[:SOURce] \n
		Snippet: value: str = driver.source.voltage.sense.get_source() \n
		Sets remote sense detection. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:VOLTage:SENSe:SOURce?')
		return trim_str_response(response)

	def set_source(self, arg_0: str) -> None:
		"""SCPI: [SOURce]:VOLTage:SENSe[:SOURce] \n
		Snippet: driver.source.voltage.sense.set_source(arg_0 = r1) \n
		Sets remote sense detection. \n
			:param arg_0:
				- AUTO: If remote sense detection is set AUTO, the detection and enabling of the voltage sense relay automatically kicks in when the connection of remote sense wires (S+, S-) to the input of the load is applied.
				- EXT: If remote sense detection is set EXT, internal voltage sense relay in the instrument is switched on and the connection of remote sense wires (S+, S- ) to the input of the load become necessary. Failure to connect remote sense can cause overvoltage or unregulated voltage output from the R&S NGP800."""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write(f'SOURce:VOLTage:SENSe:SOURce {param}')
