from enum import Enum


# noinspection SpellCheckingInspection
class ReplaceOrKeep(Enum):
	"""2 Members, KEEP ... REPLace"""
	KEEP = 0
	REPLace = 1


# noinspection SpellCheckingInspection
class TriggerExecType(Enum):
	"""2 Members, RESet ... TRIGger"""
	RESet = 0
	TRIGger = 1


# noinspection SpellCheckingInspection
class TriggerSlope(Enum):
	"""3 Members, BOTH ... POSitive"""
	BOTH = 0
	NEGative = 1
	POSitive = 2


# noinspection SpellCheckingInspection
class TriggerType(Enum):
	"""4 Members, ADDRessed ... TOGGle"""
	ADDRessed = 0
	SEQuenced = 1
	SINGle = 2
	TOGGle = 3
