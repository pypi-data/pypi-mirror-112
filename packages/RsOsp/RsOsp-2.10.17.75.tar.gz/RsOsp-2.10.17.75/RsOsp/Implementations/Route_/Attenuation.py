from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attenuation", core, parent)

	def set(self, channel_list: str) -> None:
		"""SCPI: ROUTe:ATTenuation \n
		Snippet: driver.route.attenuation.set(channel_list = r1) \n
		Sets or queries the level of attenuation, if a step attenuator is available in the module, for example in the R&S
		OSP-B171H and in the R&S OSP-B157WN. Also, you can control attenuators by the standard command method RsOsp.Route.Close.
		set, allowing joint control of attenuators and relays, and saving their target states in joint path definitions. Similar
		to method RsOsp.Route.Close.set, the parameter <channel list> uses the following syntax:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			- sss = 000 ... n (state of the attenuator to be controlled in a module)
			- ee = 01 ... m (element number of the attenuator to be controlled)
		For example, in the R&S OSP-B171H:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- sss = 000 ... 015 (attenuator steps)
			- ee = 01 ... 02 (attenuator number in module version .42) ee = 01 ... 04 (attenuator number in module version .44)
		Note that in the string 'sss', you can omit leading zeros. \n
			:param channel_list: Channel list string as described above, selecting a module and attenuator and specifying the attenuation level to be set. The query also requires the element number 'ee', but it ignores the state information 'sss'. You can submit the value of 'sss' as 000 (or any arbitrary 3-digit value) , or you can omit it, entering only ee. The range and interpretation of the state value sss depends on the specific attenuator used in the module. For details, refer to the module description.
		"""
		param = Conversions.value_to_str(channel_list)
		self._core.io.write(f'ROUTe:ATTenuation {param}')

	def get(self, channel_list: str) -> List[int]:
		"""SCPI: ROUTe:ATTenuation \n
		Snippet: value: List[int] = driver.route.attenuation.get(channel_list = r1) \n
		Sets or queries the level of attenuation, if a step attenuator is available in the module, for example in the R&S
		OSP-B171H and in the R&S OSP-B157WN. Also, you can control attenuators by the standard command method RsOsp.Route.Close.
		set, allowing joint control of attenuators and relays, and saving their target states in joint path definitions. Similar
		to method RsOsp.Route.Close.set, the parameter <channel list> uses the following syntax:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02)
			- sss = 000 ... n (state of the attenuator to be controlled in a module)
			- ee = 01 ... m (element number of the attenuator to be controlled)
		For example, in the R&S OSP-B171H:
			INTRO_CMD_HELP: (@FxxMyy(sssee) ) \n
			- sss = 000 ... 015 (attenuator steps)
			- ee = 01 ... 02 (attenuator number in module version .42) ee = 01 ... 04 (attenuator number in module version .44)
		Note that in the string 'sss', you can omit leading zeros. \n
			:param channel_list: Channel list string as described above, selecting a module and attenuator and specifying the attenuation level to be set. The query also requires the element number 'ee', but it ignores the state information 'sss'. You can submit the value of 'sss' as 000 (or any arbitrary 3-digit value) , or you can omit it, entering only ee. The range and interpretation of the state value sss depends on the specific attenuator used in the module. For details, refer to the module description.
			:return: attenuation_list: No help available"""
		param = Conversions.value_to_str(channel_list)
		response = self._core.io.query_bin_or_ascii_int_list(f'ROUTe:ATTenuation? {param}')
		return response

	def set_single_channel(self, channel: str) -> None:
		"""ROUTe:ATTenuation \n
			Same as set(), but you do not need to enter round brackets or the '@' character.  \n
			:param channel: example value (without quotes): 'F02M03(0101)'"""
		param = [channel]
		self.set_multiple_channels(param)

	def set_multiple_channels(self, channels: List[str]) -> None:
		"""ROUTe:ATTenuation \n
			Same as set_single_channel(), but for multiple channels  \n
			:param channels: example value (without quotes): ['F01M01(0301)', 'F02M03(0101)']"""
		param = f'(@{",".join(channels)})'
		self.set(param)

	def get_single_channel(self, channel: str) -> List[int]:
		"""ROUTe:ATTenuation \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param channel: example value (without quotes): 'F01M03(0001,0002,0003,0004)'"""
		param = [channel]
		return self.get_multiple_channels(param)

	def get_multiple_channels(self, channels: List[str]) -> List[int]:
		"""ROUTe:ATTenuation \n
		Same as get_single_channel(), but for multiple channels. \n
			:param channels: Example value (without quotes): ['F01M03(0002)', 'F01M04(0003)']"""
		param = f'(@{",".join(channels)})'
		return self.get(param)
