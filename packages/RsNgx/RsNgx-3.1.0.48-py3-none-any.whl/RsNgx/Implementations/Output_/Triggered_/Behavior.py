from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Behavior:
	"""Behavior commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("behavior", core, parent)

	def set(self, arg_0: str) -> None:
		"""SCPI: OUTPut:TRIGgered:BEHavior \n
		Snippet: driver.output.triggered.behavior.set(arg_0 = r1) \n
		Sets or queries output behavior when a trigger event occurs. \n
			:param arg_0: ON | OFF | GATed | list ON Output is set on when a trigger event occurs. OFF Output is set off when a trigger event occurs. GATed Output is set gated when a trigger event occurs.
		"""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write_with_opc(f'OUTPut:TRIGgered:BEHavior {param}')

	def get(self) -> str:
		"""SCPI: OUTPut:TRIGgered:BEHavior \n
		Snippet: value: str = driver.output.triggered.behavior.get() \n
		Sets or queries output behavior when a trigger event occurs. \n
			:return: arg_0: ON | OFF | GATed | list ON Output is set on when a trigger event occurs. OFF Output is set off when a trigger event occurs. GATed Output is set gated when a trigger event occurs."""
		response = self._core.io.query_str_with_opc(f'OUTPut:TRIGgered:BEHavior?')
		return trim_str_response(response)
