from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Text:
	"""Text commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("text", core, parent)

	def set_data(self, custom_message: str) -> None:
		"""SCPI: DISPlay[:WINDow]:TEXT[:DATA] \n
		Snippet: driver.display.window.text.set_data(custom_message = '1') \n
		Shows the text message box on the front display. \n
			:param custom_message: New value for text message box.
		"""
		param = Conversions.value_to_quoted_str(custom_message)
		self._core.io.write(f'DISPlay:WINDow:TEXT:DATA {param}')

	def clear(self) -> None:
		"""SCPI: DISPlay[:WINDow]:TEXT:CLEar \n
		Snippet: driver.display.window.text.clear() \n
		Clears the text message box on the front display. \n
		"""
		self._core.io.write(f'DISPlay:WINDow:TEXT:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: DISPlay[:WINDow]:TEXT:CLEar \n
		Snippet: driver.display.window.text.clear_with_opc() \n
		Clears the text message box on the front display. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsNgx.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DISPlay:WINDow:TEXT:CLEar')
