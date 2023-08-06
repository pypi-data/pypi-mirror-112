from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Define:
	"""Define commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("define", core, parent)

	@property
	def entry(self):
		"""entry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_entry'):
			from .Define_.Entry import Entry
			self._entry = Entry(self._core, self._base)
		return self._entry

	def get_all(self) -> List[str]:
		"""SCPI: TRIGger:SEQuence:DEFine:ALL \n
		Snippet: value: List[str] = driver.trigger.sequence.define.get_all() \n
		Sets several or all paths for the sequenced trigger. The query returns all path names. \n
			:return: path_name: No help available
		"""
		response = self._core.io.query_str('TRIGger:SEQuence:DEFine:ALL?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)

	def set_all(self, path_name: List[str]) -> None:
		"""SCPI: TRIGger:SEQuence:DEFine:ALL \n
		Snippet: driver.trigger.sequence.define.set_all(path_name = ['1', '2', '3']) \n
		Sets several or all paths for the sequenced trigger. The query returns all path names. \n
			:param path_name: Specifies all path names for the trigger sequence. Separate the path names by commas and write each path name in quotation marks.
		"""
		param = Conversions.list_to_csv_quoted_str(path_name)
		self._core.io.write(f'TRIGger:SEQuence:DEFine:ALL {param}')

	def get_length(self) -> int:
		"""SCPI: TRIGger:SEQuence:DEFine:LENGth \n
		Snippet: value: int = driver.trigger.sequence.define.get_length() \n
		Sets or queries the length of the sequence for the Sequenced trigger. \n
			:return: length: No help available
		"""
		response = self._core.io.query_str('TRIGger:SEQuence:DEFine:LENGth?')
		return Conversions.str_to_int(response)

	def set_length(self, length: int) -> None:
		"""SCPI: TRIGger:SEQuence:DEFine:LENGth \n
		Snippet: driver.trigger.sequence.define.set_length(length = 1) \n
		Sets or queries the length of the sequence for the Sequenced trigger. \n
			:param length: No help available
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'TRIGger:SEQuence:DEFine:LENGth {param}')
