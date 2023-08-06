from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Communicate:
	"""Communicate commands group definition. 26 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("communicate", core, parent)

	@property
	def socket(self):
		"""socket commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_socket'):
			from .Communicate_.Socket import Socket
			self._socket = Socket(self._core, self._base)
		return self._socket

	@property
	def wlan(self):
		"""wlan commands group. 2 Sub-classes, 7 commands."""
		if not hasattr(self, '_wlan'):
			from .Communicate_.Wlan import Wlan
			self._wlan = Wlan(self._core, self._base)
		return self._wlan

	@property
	def lan(self):
		"""lan commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_lan'):
			from .Communicate_.Lan import Lan
			self._lan = Lan(self._core, self._base)
		return self._lan
