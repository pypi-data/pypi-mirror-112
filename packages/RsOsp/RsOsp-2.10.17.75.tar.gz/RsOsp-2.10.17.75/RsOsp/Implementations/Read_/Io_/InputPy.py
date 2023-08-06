from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPy:
	"""InputPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inputPy", core, parent)

	def get(self, modules: str) -> List[int]:
		"""SCPI: READ:IO:IN \n
		Snippet: value: List[int] = driver.read.io.inputPy.get(modules = r1) \n
		Queries the states of all input channels of one or more selected modules.
			INTRO_CMD_HELP: The query applies only to modules that have I/O (input / output) channels. For example, the modules listed below have the following number of channels: \n
			- R&S OSP-B103: 16 input channels
			- R&S OSP-B104: 4 input channels
			- R&S OSP-B114: 4 input channels
		The return value is a set of single integer decimal numbers that represent the state of all queried input channels per
		module. Each integer is in the range of 0 to 65535:
			INTRO_CMD_HELP: The query applies only to modules that have I/O (input / output) channels. For example, the modules listed below have the following number of channels: \n
			- 0: all channels are logical 0 or low
			- 65535: all channels (maximum 16) are logical 1 or high, where 65535 = 216-1
		When converted to a binary number, each 1 or 0 digit shows the state of one channel. This representation starts with the
		lowest digit for channel one, up to the highest digit for channel 16. See also method RsOsp.Read.Io.InputPy.get_, method
		RsOsp.Read.Io.InputPy.get_ and method RsOsp.Read.Io.InputPy.get_. \n
			:param modules: Selects the modules that you want to query for their I/O channels. Identify the modules by their frame IDs Fxx and module numbers Myy. For a description of these parameters, refer to method RsOsp.Route.Close.set. Write the combined frame/module names FxxMyy, separated by commas, inside an expression of two brackets and the '@' sign. Do not use blank spaces or quotation marks in this expression. Example: (@F01M01,F01M06,F02M03) Only for querying one single module, you can use syntax without '(@...) ', for example: F01M01 If a module that you specify does not exist or does not support READ:IO:IN? (having no input channels) , the query returns no result and a SCPI error is generated. You can query the error with SYST:ERR?. For example, with a query READ:IO:IN? (@F01M06) , the result can be: -222,'Data out of range;Invalid index. frame F01: no module connected to M06,READ:IO:IN? F01M06' Or with a query READ:IO:IN? (@F01M03) , the result can be: -170,'Expression error;module on connector M03does not support input channels,READ:IO:IN? F01M03'
			:return: input_channel_value: Comma-separated list of integer decimal numbers that represent the queried input channel states as described above."""
		param = Conversions.value_to_str(modules)
		response = self._core.io.query_bin_or_ascii_int_list(f'READ:IO:IN? {param}')
		return response

	def get_single_module(self, module: str) -> List[int]:
		"""READ:IO:IN \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param module: example value (without quotes): 'F01M03'
			:return: input_channel_value: Comma-separated list of integer decimal numbers that represent the queried input channel states as described above."""
		param = [module]
		return self.get_multiple_modules(param)

	def get_multiple_modules(self, modules: List[str]) -> List[int]:
		"""READ:IO:IN \n
		Same as get_single_module(), but for multiple modules. \n
			:param modules: Example value (without quotes): ['F01M03', 'F01M04']"""
		param = f'(@{",".join(modules)})'
		return self.get(param)
