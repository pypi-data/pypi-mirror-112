from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 5 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_limit'):
			from .Current_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def get_value(self) -> float:
		"""SCPI: BATTery:SIMulator:CURRent \n
		Snippet: value: float = driver.battery.simulator.current.get_value() \n
		Queries the current (A) of battery simulator. \n
			:return: result: No help available
		"""
		response = self._core.io.query_str('BATTery:SIMulator:CURRent?')
		return Conversions.str_to_float(response)
