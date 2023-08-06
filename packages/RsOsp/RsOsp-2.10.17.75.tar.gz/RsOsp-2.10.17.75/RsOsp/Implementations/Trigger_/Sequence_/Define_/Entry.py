from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Entry:
	"""Entry commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("entry", core, parent)

	def set(self, index: int, path_name: str) -> None:
		"""SCPI: TRIGger:SEQuence:DEFine[:ENTRy] \n
		Snippet: driver.trigger.sequence.define.entry.set(index = 1, path_name = '1') \n
		Sets or queries the path, which is defined for the selected number in the sequence. \n
			:param index: Selects a number in the trigger sequence.
			:param path_name: Specifies the path name to be set for the selected number in the trigger sequence. Write the path name in quotation marks.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('path_name', path_name, DataType.String))
		self._core.io.write(f'TRIGger:SEQuence:DEFine:ENTRy {param}'.rstrip())

	def get(self, index: int) -> str:
		"""SCPI: TRIGger:SEQuence:DEFine[:ENTRy] \n
		Snippet: value: str = driver.trigger.sequence.define.entry.get(index = 1) \n
		Sets or queries the path, which is defined for the selected number in the sequence. \n
			:param index: Selects a number in the trigger sequence.
			:return: path_name: No help available"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'TRIGger:SEQuence:DEFine:ENTRy? {param}')
		return trim_str_response(response)
