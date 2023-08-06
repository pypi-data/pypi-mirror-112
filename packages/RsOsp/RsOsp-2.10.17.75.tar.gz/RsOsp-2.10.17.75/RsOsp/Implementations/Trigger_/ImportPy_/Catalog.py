from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, path_information: str = None) -> List[str]:
		"""SCPI: TRIGger:IMPort:CATalog \n
		Snippet: value: List[str] = driver.trigger.importPy.catalog.get(path_information = '1') \n
		Returns a list of trigger configurations that are stored in the primary switch unit's volatile memory. \n
			:param path_information: The reply is a comma-separated list of the exported trigger configuration filenames.
			:return: list_of_exp_trigger_configs: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_information', path_information, DataType.String, True))
		response = self._core.io.query_str(f'TRIGger:IMPort:CATalog? {param}'.rstrip())
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
