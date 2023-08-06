from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, channel_list: str) -> None:
		"""SCPI: ROUTe:PHASe \n
		Snippet: driver.route.phase.set(channel_list = r1) \n
		Sets or queries the phase angle, if a phase shifter is available in the module. Also, you can control phase shifters by
		the standard command method RsOsp.Route.Close.set, allowing joint control of phase shifters and relays, and saving their
		target states in joint path definitions. Similar to method RsOsp.Route.Close.set, the parameter <channel list> uses the
		following syntax:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			- sss = 000 ... n (state of the phase shifter to be controlled in a module)
			- ee = 01 ... m (element number of the phase shifter to be controlled)
		Note that in the string 'sss', you can omit leading zeros. \n
			:param channel_list: Channel list string as described above, selecting a module and phase shifter and specifying the phase angle to be set. The query also requires the element number 'ee', but it ignores the state information 'sss'. You can submit the value of 'sss' as 000 (or any arbitrary 3-digit value) , or you can omit it, entering only ee. The range and interpretation of the state value sss depends on the specific phase shifter used in the module. For details, refer to the module description.
		"""
		param = Conversions.value_to_str(channel_list)
		self._core.io.write(f'ROUTe:PHASe {param}')

	def get(self, channel_list: str) -> List[int]:
		"""SCPI: ROUTe:PHASe \n
		Snippet: value: List[int] = driver.route.phase.get(channel_list = r1) \n
		Sets or queries the phase angle, if a phase shifter is available in the module. Also, you can control phase shifters by
		the standard command method RsOsp.Route.Close.set, allowing joint control of phase shifters and relays, and saving their
		target states in joint path definitions. Similar to method RsOsp.Route.Close.set, the parameter <channel list> uses the
		following syntax:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			- sss = 000 ... n (state of the phase shifter to be controlled in a module)
			- ee = 01 ... m (element number of the phase shifter to be controlled)
		Note that in the string 'sss', you can omit leading zeros. \n
			:param channel_list: Channel list string as described above, selecting a module and phase shifter and specifying the phase angle to be set. The query also requires the element number 'ee', but it ignores the state information 'sss'. You can submit the value of 'sss' as 000 (or any arbitrary 3-digit value) , or you can omit it, entering only ee. The range and interpretation of the state value sss depends on the specific phase shifter used in the module. For details, refer to the module description.
			:return: phase_list: No help available"""
		param = Conversions.value_to_str(channel_list)
		response = self._core.io.query_bin_or_ascii_int_list(f'ROUTe:PHASe? {param}')
		return response

	def get_single_channel(self, channel: str) -> List[int]:
		"""ROUTe:PHASe \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param channel: example value (without quotes): 'F01M03(0001,0002,0003,0004)'"""
		param = [channel]
		return self.get_multiple_channels(param)

	def get_multiple_channels(self, channels: List[str]) -> List[int]:
		"""ROUTe:PHASe \n
		Same as get_single_channel(), but for multiple channels. \n
			:param channels: Example value (without quotes): ['F01M03(0002)', 'F01M04(0003)']"""
		param = f'(@{",".join(channels)})'
		return self.get(param)
