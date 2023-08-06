from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 13 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Current_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def protection(self):
		"""protection commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_protection'):
			from .Current_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection

	@property
	def negative(self):
		"""negative commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_negative'):
			from .Current_.Negative import Negative
			self._negative = Negative(self._core, self._base)
		return self._negative

	def get_range(self) -> float:
		"""SCPI: [SOURce]:CURRent:RANGe \n
		Snippet: value: float = driver.source.current.get_range() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('SOURce:CURRent:RANGe?')
		return Conversions.str_to_float(response)

	def set_range(self, arg_0: float) -> None:
		"""SCPI: [SOURce]:CURRent:RANGe \n
		Snippet: driver.source.current.set_range(arg_0 = 1.0) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.decimal_value_to_str(arg_0)
		self._core.io.write(f'SOURce:CURRent:RANGe {param}')
