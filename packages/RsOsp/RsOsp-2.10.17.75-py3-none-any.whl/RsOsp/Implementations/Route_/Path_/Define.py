from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Define:
	"""Define commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("define", core, parent)

	def set(self, path_name: str, channel_list: str) -> None:
		"""SCPI: ROUTe:PATH[:DEFine] \n
		Snippet: driver.route.path.define.set(path_name = '1', channel_list = r1) \n
		method RsOsp.Route.Path.Define.set or method RsOsp.Route.Path.Define.set defines a path name and the channel-list string
		that can be replaced by this path name. A short path name can thus represent a long list of specific states of relays and
		I/O channels. Use method RsOsp.Route.Close.set to switch a path. The query returns the channel list that encodes the
		defined states for all relays and I/O channels in this path. Note that in 'Compatibility Mode', the query returns a
		string with syntax that differs from the channel list (see query example below) . \n
			:param path_name: String parameter to specify the name of the path to be defined or queried. Limited to a maximum of 35 characters. Write the path name in quotation marks. The firmware observes capitalization of the path name. For example, 'path a' in lower case is not the same as 'Path A' in upper and lower case. A newly defined path name only exists in the instruments internal volatile memory (RAM) . At shutdown, all path definitions are saved permanently in the instrument’s flash memory At startup, all saved path definitions are restored automatically. All new path definitions, which you made since the last startup, are lost, if you switch off the device by the rear on/off switch. The same holds true, if you switch off the device by pushing the front PWR key for more than 10 seconds, or if the firmware crashes. You can trigger immediate storing of all defined path names in the instrument’s flash memory by using the command method RsOsp.Route.Path.export.
			:param channel_list: List of relays and I/O channels and their states to be set, as described in method RsOsp.Route.Close.set.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_name', path_name, DataType.String), ArgSingle('channel_list', channel_list, DataType.RawString))
		self._core.io.write(f'ROUTe:PATH:DEFine {param}'.rstrip())

	def get(self, path_name: str) -> str:
		"""SCPI: ROUTe:PATH[:DEFine] \n
		Snippet: value: str = driver.route.path.define.get(path_name = '1') \n
		method RsOsp.Route.Path.Define.set or method RsOsp.Route.Path.Define.set defines a path name and the channel-list string
		that can be replaced by this path name. A short path name can thus represent a long list of specific states of relays and
		I/O channels. Use method RsOsp.Route.Close.set to switch a path. The query returns the channel list that encodes the
		defined states for all relays and I/O channels in this path. Note that in 'Compatibility Mode', the query returns a
		string with syntax that differs from the channel list (see query example below) . \n
			:param path_name: String parameter to specify the name of the path to be defined or queried. Limited to a maximum of 35 characters. Write the path name in quotation marks. The firmware observes capitalization of the path name. For example, 'path a' in lower case is not the same as 'Path A' in upper and lower case. A newly defined path name only exists in the instruments internal volatile memory (RAM) . At shutdown, all path definitions are saved permanently in the instrument’s flash memory At startup, all saved path definitions are restored automatically. All new path definitions, which you made since the last startup, are lost, if you switch off the device by the rear on/off switch. The same holds true, if you switch off the device by pushing the front PWR key for more than 10 seconds, or if the firmware crashes. You can trigger immediate storing of all defined path names in the instrument’s flash memory by using the command method RsOsp.Route.Path.export.
			:return: channel_list: List of relays and I/O channels and their states to be set, as described in method RsOsp.Route.Close.set."""
		param = Conversions.value_to_quoted_str(path_name)
		response = self._core.io.query_str(f'ROUTe:PATH:DEFine? {param}')
		return trim_str_response(response)

	def set_single_channel(self, path_name: str, channel: str) -> None:
		"""ROUTe:PATH[:DEFine] \n
			Same as set(), but you do not need to enter round brackets or the '@' character.  \n
			:param path_name: String parameter to specify the name of the path to be defined
			:param channel: example value (without quotes): 'F02M03(0101)'"""
		param = [channel]
		self.set_multiple_channels(path_name, param)

	from typing import List

	def set_multiple_channels(self, path_name: str, channels: List[str]) -> None:
		"""ROUTe:PATH[:DEFine] \n
			Same as set_single_channel(), but for multiple channels  \n
			:param path_name: String parameter to specify the name of the path to be defined
			:param channels: example value (without quotes): ['F01M01(0301)', 'F02M03(0101)']"""
		param = f'(@{",".join(channels)})'
		self.set(path_name, param)
