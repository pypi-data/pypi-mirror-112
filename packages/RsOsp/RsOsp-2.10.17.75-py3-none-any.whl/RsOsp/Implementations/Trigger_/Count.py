from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def get_value(self) -> int:
		"""SCPI: TRIGger:COUNt[:VALue] \n
		Snippet: value: int = driver.trigger.count.get_value() \n
		Queries the trigger count, hence the number of executed trigger events since the last activation of the trigger
		functionality. \n
			:return: count: No help available
		"""
		response = self._core.io.query_str('TRIGger:COUNt:VALue?')
		return Conversions.str_to_int(response)

	def get_overflow(self) -> bool:
		"""SCPI: TRIGger:COUNt:OVERflow \n
		Snippet: value: bool = driver.trigger.count.get_overflow() \n
		Queries, if a trigger overflow has happened since the last activation of the trigger functionality. If the trigger input
		connectors of the switch unit receive input signals faster than the firmware can process, it cannot count all trigger
		events, and it cannot update the trigger counter correctly. You can use the command to check, if this case has occurred
		since the last trigger activation. \n
			:return: overflow: No help available
		"""
		response = self._core.io.query_str('TRIGger:COUNt:OVERflow?')
		return Conversions.str_to_bool(response)
