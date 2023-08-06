from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Function:
	"""Function commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("function", core, parent)

	def set(self, modules: str, function: str) -> None:
		"""SCPI: DIAGnostic:SERVice:MODule:FUNCtion \n
		Snippet: driver.diagnostic.service.module.function.set(modules = r1, function = '1') \n
		No command help available \n
			:param modules: No help available
			:param function: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('modules', modules, DataType.RawString), ArgSingle('function', function, DataType.String))
		self._core.io.write(f'DIAGnostic:SERVice:MODule:FUNCtion {param}'.rstrip())

	def get(self, modules: str, function: str) -> List[str]:
		"""SCPI: DIAGnostic:SERVice:MODule:FUNCtion \n
		Snippet: value: List[str] = driver.diagnostic.service.module.function.get(modules = r1, function = '1') \n
		No command help available \n
			:param modules: No help available
			:param function: No help available
			:return: response: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('modules', modules, DataType.RawString), ArgSingle('function', function, DataType.String))
		response = self._core.io.query_str(f'DIAGnostic:SERVice:MODule:FUNCtion? {param}'.rstrip())
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
