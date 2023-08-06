from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Beeper:
	"""Beeper commands group definition. 8 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("beeper", core, parent)

	@property
	def protection(self):
		"""protection commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_protection'):
			from .Beeper_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .Beeper_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Beeper_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def complete(self):
		"""complete commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_complete'):
			from .Beeper_.Complete import Complete
			self._complete = Complete(self._core, self._base)
		return self._complete

	@property
	def warningPy(self):
		"""warningPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_warningPy'):
			from .Beeper_.WarningPy import WarningPy
			self._warningPy = WarningPy(self._core, self._base)
		return self._warningPy
