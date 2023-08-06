from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Link:
	"""Link commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("link", core, parent)

	def set(self, arg_0: int) -> None:
		"""SCPI: [SOURce]:CURRent:PROTection:LINK \n
		Snippet: driver.source.current.protection.link.set(arg_0 = 1) \n
		Sets or queries the fuses of several selected channels (fuse linking) . \n
			:param arg_0: 1 | 2
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SOURce:CURRent:PROTection:LINK {param}')

	def get(self, arg_0: int) -> int:
		"""SCPI: [SOURce]:CURRent:PROTection:LINK \n
		Snippet: value: int = driver.source.current.protection.link.get(arg_0 = 1) \n
		Sets or queries the fuses of several selected channels (fuse linking) . \n
			:param arg_0: 1 | 2
			:return: arg_0: 1 | 2"""
		param = Conversions.decimal_value_to_str(arg_0)
		response = self._core.io.query_str(f'SOURce:CURRent:PROTection:LINK? {param}')
		return Conversions.str_to_int(response)
