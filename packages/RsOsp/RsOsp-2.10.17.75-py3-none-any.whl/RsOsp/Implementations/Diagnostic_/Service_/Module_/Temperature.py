from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Temperature:
	"""Temperature commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("temperature", core, parent)

	def get(self, modules: str) -> List[float]:
		"""SCPI: DIAGnostic:SERVice:MODule:TEMPerature \n
		Snippet: value: List[float] = driver.diagnostic.service.module.temperature.get(modules = r1) \n
		Queries the temperature of selected modules in degrees centigrade. \n
			:param modules: The command addresses the modules by the following syntax, like the module names string in method RsOsp.Read.Io.InputPy.get_: xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01) yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			:return: temperature_value: No help available"""
		param = Conversions.value_to_str(modules)
		response = self._core.io.query_bin_or_ascii_float_list(f'DIAGnostic:SERVice:MODule:TEMPerature? {param}')
		return response
