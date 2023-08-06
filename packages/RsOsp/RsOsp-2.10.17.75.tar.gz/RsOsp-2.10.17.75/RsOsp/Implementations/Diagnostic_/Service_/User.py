from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def get_error(self) -> List[str]:
		"""SCPI: DIAGnostic:SERVice:USER:ERRor \n
		Snippet: value: List[str] = driver.diagnostic.service.user.get_error() \n
		Queries for device errors that were not necessarily evoked by a remote control command. Typically, use this query for
		errors that may have come up during booting. \n
			:return: user_error_list: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:SERVice:USER:ERRor?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)

	def get_warning_py(self) -> List[str]:
		"""SCPI: DIAGnostic:SERVice:USER:WARNing \n
		Snippet: value: List[str] = driver.diagnostic.service.user.get_warning_py() \n
		Queries for device warnings that were not necessarily evoked by a remote control command. Typically, use this query for
		warnings that may have come up during booting. \n
			:return: user_warning_list: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:SERVice:USER:WARNing?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
