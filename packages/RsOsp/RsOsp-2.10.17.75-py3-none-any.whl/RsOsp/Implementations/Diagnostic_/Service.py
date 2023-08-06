from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Service:
	"""Service commands group definition. 6 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("service", core, parent)

	@property
	def module(self):
		"""module commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_module'):
			from .Service_.Module import Module
			self._module = Module(self._core, self._base)
		return self._module

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_user'):
			from .Service_.User import User
			self._user = User(self._core, self._base)
		return self._user

	def get_hw_info(self) -> List[str]:
		"""SCPI: DIAGnostic:SERVice:HWINfo \n
		Snippet: value: List[str] = driver.diagnostic.service.get_hw_info() \n
		Returns information about all hardware components (motherboards and modules) that are part of the complete system of one
		or several R&S OSP instruments.
			INTRO_CMD_HELP: The returned component information consists of: \n
			- Location ID (= switch unit and module number, for example, frame F01 is the primary device, frame F02 is the first secondary device, M00 is the primary device's motherboard, M01 is the module connected to the connector M01)
			- Name (for example, OSPMAINBOARD, OSP220, OSP230, OSP320, OSP-B101)
			- Serial number (for example, 100173)
			- Part number (= order number, for example, 1528.3105.03)
			- Hardware code:
			INTRO_CMD_HELP: The returned component information consists of: \n
			- Modules that are controlled via 1 module bus typically return the code 0
			- Modules that are controlled via 2 module buses return the codes 1 for the first control board and 2 for the second control board
			- Product index (model iteration of a hardware version, for example, 01.00) \n
			:return: hw_info_list: The response is a string in following format: location|name|sn_nbr|part_nbr| hardware_code|product_index
		"""
		response = self._core.io.query_str('DIAGnostic:SERVice:HWINfo?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)
