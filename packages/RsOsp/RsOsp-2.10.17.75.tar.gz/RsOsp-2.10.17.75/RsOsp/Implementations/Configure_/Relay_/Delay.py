from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, channel_list: str) -> None:
		"""SCPI: CONFigure:RELay:DELay \n
		Snippet: driver.configure.relay.delay.set(channel_list = r1) \n
		Sets or queries the command delay times for up to 4 external power-transfer relays connected to the R&S OSP-B104 Digital
		I/O Module (EMS) . The delay determines the period of time, which is reserved for a relay to change its state. Note that
		these external relays require switching times that are significantly longer than in most other relays. After receiving a
		method RsOsp.Route.Close.set command for changing the state of a connected external relay, the module R&S OSP-B104
		behaves as follows:
			INTRO_CMD_HELP: Saves all configuration settings to a backup file. These settings comprise the following: \n
			- It sends the switching pulse during this full period of time
			- Then it queries the relay's current position
			- If the current position differs from the target position, the module generates a SCPI error, which is available via SYST:ERR?
			- Then it accepts the next command
		You can set delay times to ensure that the switching process of external transfer relays is completed, before further
		commands are executed. If you modify a delay time, the new value is stored durable on the module's EEPROM memory. \n
			:param channel_list: List of external transfer relays (connected to module R&S OSP-B104) and associated delay times to be set or queried.
				- (@FxxMyy(sssee) ): Defines the channel list for one relay with the following parameters:FxxMyy: as described in ROUTe:CLOSe.sss = 0 to 255. The digits in front of the last 2 digits (hence, the 1, 2 or 3 leading digits in the parenthesis) represent the 8-bit delay value. The adjustable delay time has a resolution of 50 ms and spans from 0 to 12.75 seconds (255 x 50 ms = 12750 ms) . The default value 2 is equivalent to a delay time of 100 ms.ee = 11, 12, 13, 14. The last 2 digits in the parenthesis represent the numbers ('names') of the relays (up to 4) that are connected to the R&S OSP-B104. The numeral offset of 10 distinguishes these relay numbers from the I/O channel numbers 01 to 04 on the same module."""
		param = Conversions.value_to_str(channel_list)
		self._core.io.write(f'CONFigure:RELay:DELay {param}')

	def get(self, channel_list: str) -> List[int]:
		"""SCPI: CONFigure:RELay:DELay \n
		Snippet: value: List[int] = driver.configure.relay.delay.get(channel_list = r1) \n
		Sets or queries the command delay times for up to 4 external power-transfer relays connected to the R&S OSP-B104 Digital
		I/O Module (EMS) . The delay determines the period of time, which is reserved for a relay to change its state. Note that
		these external relays require switching times that are significantly longer than in most other relays. After receiving a
		method RsOsp.Route.Close.set command for changing the state of a connected external relay, the module R&S OSP-B104
		behaves as follows:
			INTRO_CMD_HELP: Saves all configuration settings to a backup file. These settings comprise the following: \n
			- It sends the switching pulse during this full period of time
			- Then it queries the relay's current position
			- If the current position differs from the target position, the module generates a SCPI error, which is available via SYST:ERR?
			- Then it accepts the next command
		You can set delay times to ensure that the switching process of external transfer relays is completed, before further
		commands are executed. If you modify a delay time, the new value is stored durable on the module's EEPROM memory. \n
			:param channel_list: List of external transfer relays (connected to module R&S OSP-B104) and associated delay times to be set or queried.
				- (@FxxMyy(sssee) ): Defines the channel list for one relay with the following parameters:FxxMyy: as described in ROUTe:CLOSe.sss = 0 to 255. The digits in front of the last 2 digits (hence, the 1, 2 or 3 leading digits in the parenthesis) represent the 8-bit delay value. The adjustable delay time has a resolution of 50 ms and spans from 0 to 12.75 seconds (255 x 50 ms = 12750 ms) . The default value 2 is equivalent to a delay time of 100 ms.ee = 11, 12, 13, 14. The last 2 digits in the parenthesis represent the numbers ('names') of the relays (up to 4) that are connected to the R&S OSP-B104. The numeral offset of 10 distinguishes these relay numbers from the I/O channel numbers 01 to 04 on the same module.
			:return: delay_factor_list: No help available"""
		param = Conversions.value_to_str(channel_list)
		response = self._core.io.query_bin_or_ascii_int_list(f'CONFigure:RELay:DELay? {param}')
		return response
