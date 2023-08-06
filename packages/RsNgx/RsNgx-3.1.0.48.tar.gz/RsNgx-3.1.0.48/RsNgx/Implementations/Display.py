from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	@property
	def window(self):
		"""window commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Display_.Window import Window
			self._window = Window(self._core, self._base)
		return self._window

	def get_brightness(self) -> float:
		"""SCPI: DISPlay:BRIGhtness \n
		Snippet: value: float = driver.display.get_brightness() \n
		Sets or queries the display brightness. \n
			:return: display_brightness: No help available
		"""
		response = self._core.io.query_str('DISPlay:BRIGhtness?')
		return Conversions.str_to_float(response)

	def set_brightness(self, display_brightness: float) -> None:
		"""SCPI: DISPlay:BRIGhtness \n
		Snippet: driver.display.set_brightness(display_brightness = 1.0) \n
		Sets or queries the display brightness. \n
			:param display_brightness: Displays brightness for the instrument.
		"""
		param = Conversions.decimal_value_to_str(display_brightness)
		self._core.io.write(f'DISPlay:BRIGhtness {param}')
