from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Default:
	"""Default commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("default", core, parent)

	def save(self, file_path: str = None) -> None:
		"""SCPI: SYSTem:SETTing:DEFault:SAVE \n
		Snippet: driver.system.setting.default.save(file_path = '1') \n
		No command help available \n
			:param file_path: No help available
		"""
		param = ''
		if file_path:
			param = Conversions.value_to_quoted_str(file_path)
		self._core.io.write(f'SYSTem:SETTing:DEFault:SAVE {param}'.strip())
