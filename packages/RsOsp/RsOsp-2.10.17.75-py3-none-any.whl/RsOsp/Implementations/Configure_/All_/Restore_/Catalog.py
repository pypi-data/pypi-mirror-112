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

	def get(self, restore_file_info: str = None) -> List[str]:
		"""SCPI: CONFigure:ALL:RESTore:CATalog \n
		Snippet: value: List[str] = driver.configure.all.restore.catalog.get(restore_file_info = '1') \n
		Queries the names of all backup files that are stored in the switch unit's internal flash memory. Each of these backup
		files comprises a full set of switch unit settings. All configuration filenames have the extension '.backup'.
		Do not enter the extension when specifying a filename. A filename query does not return the extension. For example, when
		you save the 'Interconnection' definition file 'settings-2018-10-25', it is saved as 'settings-2018-10-25.backup'.
		A query returns this filename as 'settings-2018-10-25', only. \n
			:param restore_file_info: No help available
			:return: list_of_backup_files: Comma-separated list of filenames, each in quotation marks. If no files exist, an empty string '' is returned."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('restore_file_info', restore_file_info, DataType.String, True))
		response = self._core.io.query_str(f'CONFigure:ALL:RESTore:CATalog? {param}'.rstrip())
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
