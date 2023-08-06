from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Close:
	"""Close commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("close", core, parent)

	def set(self, channel_list_or_path_name: str) -> None:
		"""SCPI: ROUTe:CLOSe \n
		Snippet: driver.route.close.set(channel_list_or_path_name = r1) \n
		Sets or queries the state of selected relays or I/O channels. The query returns a 1 for each physical state of a queried
		relay or channel that is identical with the state specified in the channel list. If the physical state of a queried relay
		or channel differs from the state specified in the list, the query returns a 0. Note that for failsafe (monostable)
		relays, the query returns the state of the control line, only, while for latched (bistable) relays, the query always
		reads the true physical switching state. The parameter <channel list or path name> is also called the 'channel list
		string'. Its basic syntax is as follows: (@FxxMyy(sssee) ) Defines the channel list for just one relay or I/O channel,
		with the following parameters:
			INTRO_CMD_HELP: For example, the following solid-state relay (SSR) modules and digital I/O modules have no switching counter: \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02) Note that the slot position is labeled with an M, although in the hardware the actual positions are either FS (front slot) or RS (rear slot) . Using M instead reflects the fact that the firmware can detect only to the motherboard connector, to which a module is connected. The actual front or rear mounting position is not detected. In a factory configuration, the correlation of slot positions and connectors follows the scheme in Figure 'Top view of the motherboard with its connectors for module bus cables'. If you mount modules yourself, we recommend using the same correlation. Also note that the modules are addressed by the syntax M0x, as opposed to the syntax A1x that was used for the legacy switch units R&S OSP1x0. Setting commands accept both syntax versions, M0x or A1x. For query commands, to change from one to the other syntax version, use the command method RsOsp.Configure.Compatible.mode.
			- sss = 000 ... n (state of the element to be controlled in a module) The element can be a relay, an output channel or another Switchable item. Some system-specific or customer-specific modules can have different elements. In the string 'sss', you can omit leading zeros. Hence, '(@FxxMyy(ssee) )' for double-digit states or '(@FxxMyy(see) )' for single-digit states are permissible. The number of available states depends on the module type. Examples are 0 to 1 (for SPDT, DPDT and DP3T relays or I/O channels) , 0 to 6 (for SP6T and 4P6T) , or 0 to 8 (for SP8T) . Some modules, for example the 'R&S OSP-B104 Digital I/O Module (EMS) ', use sss to set a 3-digit state like the delay time. For details, refer to the description of the module.
			- ee = 01 ... m (number of the element to be controlled in a module) The number of available elements depends on the module type. Examples are 01 to 06 for the 6 SPDT relays in module R&S OSP-B101 or 01 to 16 for the 16 output channels in module R&S OSP-B103.
		Some special modules also allow a different format, for example eee, if selecting the element requires 3 digits.
		For details, refer to the description of the module. If you want to address a series of relays or channels in the command
		method RsOsp.Route.Close.set, you can use one of the following concatenated syntax formats: (@FxxMyy(ssee) ,FxxMyy(ssee) ,
		FxxMyy(ssee) ,...) Sets selected relays or channels in selected modules of selected switch units to the specified state.
		(In each element of the channel list, replace the parameters xx, yy, ss and ee with arbitrary numbers according to your
		needs.) Or concatenate addressing several relays or channels within a selected module: (@FxxMyy(sxex,syey,szez,...
		) ) Sets several relays or channels (with numbers ex, ey, ez, ...) in one module to individual states (sx, sy, sz, ...) .
		For example, ROUT:CLOS (@F01M11(0102,0104,0105) ) sets relays 2, 4 & 5 to state 1. (@FxxMyy(ssee:ssff) ) Sets a
		continuous range of relays or channels in one module to the same state, with ff = ee + number of continuous relays. For
		example, ROUT:CLOS (@F01M11(0101:0105) ) is equal to ROUT:CLOS (@F01M11(0101,0102,0103,0104,0105) ). \n
			:param channel_list_or_path_name: Channel list string as described above, specifying relays or channels and their states to be set or queried. Instead of an explicit channel list string, you can use a 'path name' (in quotation marks) , previously defined by method RsOsp.Route.Path.Define.set.
		"""
		param = Conversions.value_to_str(channel_list_or_path_name)
		self._core.io.write(f'ROUTe:CLOSe {param}')

	def get(self, channel_list_or_path_name: str) -> List[bool]:
		"""SCPI: ROUTe:CLOSe \n
		Snippet: value: List[bool] = driver.route.close.get(channel_list_or_path_name = r1) \n
		Sets or queries the state of selected relays or I/O channels. The query returns a 1 for each physical state of a queried
		relay or channel that is identical with the state specified in the channel list. If the physical state of a queried relay
		or channel differs from the state specified in the list, the query returns a 0. Note that for failsafe (monostable)
		relays, the query returns the state of the control line, only, while for latched (bistable) relays, the query always
		reads the true physical switching state. The parameter <channel list or path name> is also called the 'channel list
		string'. Its basic syntax is as follows: (@FxxMyy(sssee) ) Defines the channel list for just one relay or I/O channel,
		with the following parameters:
			INTRO_CMD_HELP: For example, the following solid-state relay (SSR) modules and digital I/O modules have no switching counter: \n
			- xx = 01, 02, 03,...,99 (frame ID in, e.g., switch unit name F01)
			- yy = 01, 02, 03,...,20 (module ID in, e.g., slot position M02) Note that the slot position is labeled with an M, although in the hardware the actual positions are either FS (front slot) or RS (rear slot) . Using M instead reflects the fact that the firmware can detect only to the motherboard connector, to which a module is connected. The actual front or rear mounting position is not detected. In a factory configuration, the correlation of slot positions and connectors follows the scheme in Figure 'Top view of the motherboard with its connectors for module bus cables'. If you mount modules yourself, we recommend using the same correlation. Also note that the modules are addressed by the syntax M0x, as opposed to the syntax A1x that was used for the legacy switch units R&S OSP1x0. Setting commands accept both syntax versions, M0x or A1x. For query commands, to change from one to the other syntax version, use the command method RsOsp.Configure.Compatible.mode.
			- sss = 000 ... n (state of the element to be controlled in a module) The element can be a relay, an output channel or another Switchable item. Some system-specific or customer-specific modules can have different elements. In the string 'sss', you can omit leading zeros. Hence, '(@FxxMyy(ssee) )' for double-digit states or '(@FxxMyy(see) )' for single-digit states are permissible. The number of available states depends on the module type. Examples are 0 to 1 (for SPDT, DPDT and DP3T relays or I/O channels) , 0 to 6 (for SP6T and 4P6T) , or 0 to 8 (for SP8T) . Some modules, for example the 'R&S OSP-B104 Digital I/O Module (EMS) ', use sss to set a 3-digit state like the delay time. For details, refer to the description of the module.
			- ee = 01 ... m (number of the element to be controlled in a module) The number of available elements depends on the module type. Examples are 01 to 06 for the 6 SPDT relays in module R&S OSP-B101 or 01 to 16 for the 16 output channels in module R&S OSP-B103.
		Some special modules also allow a different format, for example eee, if selecting the element requires 3 digits.
		For details, refer to the description of the module. If you want to address a series of relays or channels in the command
		method RsOsp.Route.Close.set, you can use one of the following concatenated syntax formats: (@FxxMyy(ssee) ,FxxMyy(ssee) ,
		FxxMyy(ssee) ,...) Sets selected relays or channels in selected modules of selected switch units to the specified state.
		(In each element of the channel list, replace the parameters xx, yy, ss and ee with arbitrary numbers according to your
		needs.) Or concatenate addressing several relays or channels within a selected module: (@FxxMyy(sxex,syey,szez,...
		) ) Sets several relays or channels (with numbers ex, ey, ez, ...) in one module to individual states (sx, sy, sz, ...) .
		For example, ROUT:CLOS (@F01M11(0102,0104,0105) ) sets relays 2, 4 & 5 to state 1. (@FxxMyy(ssee:ssff) ) Sets a
		continuous range of relays or channels in one module to the same state, with ff = ee + number of continuous relays. For
		example, ROUT:CLOS (@F01M11(0101:0105) ) is equal to ROUT:CLOS (@F01M11(0101,0102,0103,0104,0105) ). \n
			:param channel_list_or_path_name: Channel list string as described above, specifying relays or channels and their states to be set or queried. Instead of an explicit channel list string, you can use a 'path name' (in quotation marks) , previously defined by method RsOsp.Route.Path.Define.set.
			:return: arg_1:
				- 1: True, the relay or channel is in the state that is indicated in the channel list.
				- 0: False, the relay or channel is not in the state indicated in the channel list."""
		param = Conversions.value_to_str(channel_list_or_path_name)
		response = self._core.io.query_str(f'ROUTe:CLOSe? {param}')
		return Conversions.str_to_bool_list(response)

	def set_single_channel(self, channel: str) -> None:
		"""ROUTe:CLOSe \n
			Same as set(), but you do not need to enter round brackets or the '@' character.  \n
			:param channel: example value (without quotes): 'F01M01(0301)'"""
		param = [channel]
		self.set_multiple_channels(param)

	def set_multiple_channels(self, channels: List[str]) -> None:
		"""ROUTe:CLOSe \n
			Same as set_single_channel(), but for multiple channels  \n
			:param channels: example value (without quotes): ['F01M01(0301)', 'F02M03(0101)']"""
		param = f'(@{",".join(channels)})'
		self.set(param)

	def set_path(self, path_name: str) -> None:
		"""ROUTe:CLOSe \n
		Instead of an explicit channel list string, you can use a "pathName" previously defined by the RsOsp.Route.Path.Define.set()  \n
		:param path_name: example of the path_name (without quotes): 'PathA'"""
		param = f'"{path_name}"'
		self.set(param)

	def get_single_channel(self, channel: str) -> List[bool]:
		"""ROUTe:CLOSe \n
		Same as get(), but you do not need to enter round brackets or the '@' character. \n
			:param channel: example value (without quotes): 'F01M01(0301)'"""
		param = [channel]
		return self.get_multiple_channels(param)

	def get_multiple_channels(self, channels: List[str]) -> List[bool]:
		"""ROUTe:CLOSe \n
		Same as get_single_channel(), but for multiple channels. \n
			:param channels: Example value (without quotes): ['F01M01(0301)', 'F02M03(0101)']"""
		param = f'(@{",".join(channels)})'
		return self.get(param)

	def get_path(self, path_name: str) -> List[bool]:
		"""ROUTe:CLOSe \n
		Instead of an explicit channel list string, you can use a "pathName" previously defined by the RsOsp.Route.Path.Define.set()  \n
		:param path_name: example of the path_name (without quotes): 'PathA'
		:return: arg_1:
				- 1: True, the relay or channel is in the state that is indicated in the channel list.
				- 0: False, the relay or channel is not in the state indicated in the channel list. """
		param = f'"{path_name}"'
		return self.get(param)
