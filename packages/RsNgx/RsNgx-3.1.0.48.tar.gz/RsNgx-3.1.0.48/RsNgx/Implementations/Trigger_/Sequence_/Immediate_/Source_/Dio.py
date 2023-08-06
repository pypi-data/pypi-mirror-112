from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dio:
	"""Dio commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dio", core, parent)

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Dio_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pin'):
			from .Dio_.Pin import Pin
			self._pin = Pin(self._core, self._base)
		return self._pin
