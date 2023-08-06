from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HwInfo:
	"""HwInfo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hwInfo", core, parent)

	def set(self, modules: str) -> None:
		"""SCPI: DIAGnostic:SERVice:MODule:HWINfo \n
		Snippet: driver.diagnostic.service.module.hwInfo.set(modules = r1) \n
		The setting command can make modules update their hardware configuration. The command is implemented for all modules, but
		it was developed especially for system modules that can have submodules attached. The command allows updating such
		submodules in the firmware during operation. For modules that cannot update any hardware configuration, the command has
		no effect. The query command returns the most recently updated hardware configuration. Modules, which support this query,
		reply with an individual, module-specific return string. All other modules reply with an empty string ''. \n
			:param modules: The command addresses the modules by the following syntax, like the module names string in method RsOsp.Read.Io.InputPy.get_: xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01) yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
		"""
		param = Conversions.value_to_str(modules)
		self._core.io.write(f'DIAGnostic:SERVice:MODule:HWINfo {param}')

	def get(self, modules: str) -> List[str]:
		"""SCPI: DIAGnostic:SERVice:MODule:HWINfo \n
		Snippet: value: List[str] = driver.diagnostic.service.module.hwInfo.get(modules = r1) \n
		The setting command can make modules update their hardware configuration. The command is implemented for all modules, but
		it was developed especially for system modules that can have submodules attached. The command allows updating such
		submodules in the firmware during operation. For modules that cannot update any hardware configuration, the command has
		no effect. The query command returns the most recently updated hardware configuration. Modules, which support this query,
		reply with an individual, module-specific return string. All other modules reply with an empty string ''. \n
			:param modules: The command addresses the modules by the following syntax, like the module names string in method RsOsp.Read.Io.InputPy.get_: xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01) yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			:return: hw_info: No help available"""
		param = Conversions.value_to_str(modules)
		response = self._core.io.query_str(f'DIAGnostic:SERVice:MODule:HWINfo? {param}')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
