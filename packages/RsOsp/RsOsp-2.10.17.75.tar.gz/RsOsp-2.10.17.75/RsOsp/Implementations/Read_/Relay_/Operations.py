from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Operations:
	"""Operations commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("operations", core, parent)

	def get(self, channel_list: str) -> List[int]:
		"""SCPI: READ:RELay:OPERations \n
		Snippet: value: List[int] = driver.read.relay.operations.get(channel_list = r1) \n
		Queries the internal switching counter, which acquires the total number of operation cycles of each relay (and even of
		I/O channels) . The number of cycles is stored durable in the flash EEPROM of the module that the relay is part of.
		Storing occurs after every hour of R&S OSP operation, but only if the number has changed. Besides this time-controlled
		storing, also the query command triggers storing the counter's value. To make sure not to lose any operation cycle counts,
		we recommend sending the command method RsOsp.Read.Relay.Operations.get_ before terminating a remote control session. If
		the module that you specify does not have a switching counter, the query always returns the value '0' as the result.
			INTRO_CMD_HELP: For example, the following solid-state relay (SSR) modules and digital I/O modules have no switching counter: \n
			- R&S OSP-B103
			- R&S OSP-B107
			- R&S OSP-B127
			- R&S OSP-B128
			- R&S OSP-B142
		In the R&S OSP-B104 and R&S OSP-B114, only the electromechanical relay has a switching counter. \n
			:param channel_list: Specifies the relays and I/O channels to be read. For the channel list syntax, refer to method RsOsp.Route.Close.set.
			:return: switch_counts: The query returns a comma-separated string with a number for each relay or channel in the list, in the same order as the channel list is specified."""
		param = Conversions.value_to_str(channel_list)
		response = self._core.io.query_bin_or_ascii_int_list(f'READ:RELay:OPERations? {param}')
		return response

	def get_single_channel(self, channel: str) -> List[int]:
		"""READ:RELay:OPERations \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param channel: example value (without quotes): 'F01M03'"""
		param = [channel]
		return self.get_multiple_channels(param)

	def get_multiple_channels(self, channels: List[str]) -> List[int]:
		"""READ:RELay:OPERations \n
		Same as get_single_channel(), but for multiple channels. \n
			:param channels: Example value (without quotes): ['F01M03(0002)', 'F01M04(0003)']"""
		param = f'(@{",".join(channels)})'
		return self.get(param)
