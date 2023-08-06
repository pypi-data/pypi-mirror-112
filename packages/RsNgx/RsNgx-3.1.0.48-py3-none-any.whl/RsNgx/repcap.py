from enum import Enum
from .Internal.RepeatedCapability import VALUE_DEFAULT
from .Internal.RepeatedCapability import VALUE_EMPTY


# noinspection SpellCheckingInspection
class Channel(Enum):
	"""Repeated capability Channel \n
	Channel"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class DigitalIo(Enum):
	"""Repeated capability DigitalIo \n
	IO"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
