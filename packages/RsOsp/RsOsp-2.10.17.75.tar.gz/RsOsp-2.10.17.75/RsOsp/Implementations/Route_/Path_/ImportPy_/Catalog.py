from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, path_information: str = None) -> List[str]:
		"""SCPI: ROUTe:PATH:IMPort:CATalog \n
		Snippet: value: List[str] = driver.route.path.importPy.catalog.get(path_information = '1') \n
		Returns the names of all switching path configuration files that are stored in the switch unit's flash memory. All path
		filenames have the extension '.path'. Do not enter the extension when specifying a filename. A filename query does not
		return the extension. For example, when you save the path file 'gen-pa_1', it is saved as 'gen-pa_1.path'.
		A query returns this filename as 'gen-pa_1', only. The command MMEMory:CATalog? is equivalent with method RsOsp.Route.
		Path.ImportPy.Catalog.get_ \n
			:param path_information: No help available
			:return: list_of_exp_path_configs: Comma-separated list of filenames, each in quotation marks."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_information', path_information, DataType.String, True))
		response = self._core.io.query_str(f'ROUTe:PATH:IMPort:CATalog? {param}'.rstrip())
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
