from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interlock:
	"""Interlock commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interlock", core, parent)

	def get(self, modules: str) -> List[bool]:
		"""SCPI: READ:MODule:INTerlock \n
		Snippet: value: List[bool] = driver.read.module.interlock.get(modules = r1) \n
		Queries the interlock state of one or more selected modules.
			INTRO_CMD_HELP: The query applies only to modules that have an interlock, as in these modules: \n
			- R&S OSP-B104
			- R&S OSP-B114  \n
			:param modules: Selects the modules that you want to query for their interlock states. Identify the modules by their frame IDs Fxx and module numbers Myy. For a description of these parameters, refer to method RsOsp.Route.Close.set. Write the combined frame/module names FxxMyy, separated by commas, inside an expression of two brackets and the '@' sign. Do not use blank spaces or quotation marks in this expression. Example: (@F01M01,F01M06,F02M03) Only for querying one single module, you can use syntax without '(@...) ', for example: F01M01 If a module that you specify does not exist or does not support READ:MOD:INT? (having no interlock functionality) , the query returns no result and a SCPI error is generated. You can query the error with SYST:ERR?. For example, with a query READ:MOD:INT? (@F01M06) , the result can be: -222,'Data out of range;Invalid index. frame F01: no module connected to M06,READ:MOD:INT? F01M06' Or with a query READ:MOD:INT? (@F01M03) , the result can be: -170,'Expression error;module on connector M03does not support interlock,READ:MOD:INT? F01M03'
			:return: interlock_state: Comma-separated list of '0 | 1' values that represent the interlock states.
				- 0: The interlock of the queried module is in open state, no measurements can be made.
				- 1: The interlock of the queried module is in closed state, measurements can proceed normally."""
		param = Conversions.value_to_str(modules)
		response = self._core.io.query_str(f'READ:MODule:INTerlock? {param}')
		return Conversions.str_to_bool_list(response)

	def get_single_module(self, module: str) -> List[bool]:
		"""READ:MODule:INTerlock \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param module: example value (without quotes): 'F01M03'"""
		param = [module]
		return self.get_multiple_modules(param)

	def get_multiple_modules(self, modules: List[str]) -> List[bool]:
		"""READ:MODule:INTerlock \n
		Same as get_single_module(), but for multiple channels.
			:param modules: Example value (without quotes): ['F01M03', 'F01M04']"""
		param = f'(@{",".join(modules)})'
		return self.get(param)
