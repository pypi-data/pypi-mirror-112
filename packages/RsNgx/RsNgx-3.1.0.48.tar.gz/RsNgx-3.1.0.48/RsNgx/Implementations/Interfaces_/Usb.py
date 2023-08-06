from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usb:
	"""Usb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usb", core, parent)

	# noinspection PyTypeChecker
	def get_class(self) -> enums.UsbClass:
		"""SCPI: INTerfaces:USB:CLASs \n
		Snippet: value: enums.UsbClass = driver.interfaces.usb.get_class() \n
		Sets or queries the USB class. \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('INTerfaces:USB:CLASs?')
		return Conversions.str_to_scalar_enum(response, enums.UsbClass)

	def set_class(self, arg_0: enums.UsbClass) -> None:
		"""SCPI: INTerfaces:USB:CLASs \n
		Snippet: driver.interfaces.usb.set_class(arg_0 = enums.UsbClass.CDC) \n
		Sets or queries the USB class. \n
			:param arg_0:
				- CDC: USB CDC connection.
				- TMC: USB TMC connection."""
		param = Conversions.enum_scalar_to_str(arg_0, enums.UsbClass)
		self._core.io.write(f'INTerfaces:USB:CLASs {param}')
