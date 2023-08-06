from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Key:
	"""Key commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("key", core, parent)

	def get_brightness(self) -> float:
		"""SCPI: SYSTem:KEY:BRIGhtness \n
		Snippet: value: float = driver.system.key.get_brightness() \n
		Sets or queries the front panel key brightness. \n
			:return: front_key_brightness: No help available
		"""
		response = self._core.io.query_str('SYSTem:KEY:BRIGhtness?')
		return Conversions.str_to_float(response)

	def set_brightness(self, front_key_brightness: float) -> None:
		"""SCPI: SYSTem:KEY:BRIGhtness \n
		Snippet: driver.system.key.set_brightness(front_key_brightness = 1.0) \n
		Sets or queries the front panel key brightness. \n
			:param front_key_brightness: Sets the key brightness.
		"""
		param = Conversions.decimal_value_to_str(front_key_brightness)
		self._core.io.write(f'SYSTem:KEY:BRIGhtness {param}')
