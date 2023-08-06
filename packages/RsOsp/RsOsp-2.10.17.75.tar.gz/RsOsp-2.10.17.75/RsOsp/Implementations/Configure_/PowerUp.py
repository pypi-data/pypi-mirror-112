from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerUp:
	"""PowerUp commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("powerUp", core, parent)

	def get_path(self) -> str:
		"""SCPI: CONFigure:POWerup:PATH \n
		Snippet: value: str = driver.configure.powerUp.get_path() \n
		Sets or queries the switch-on action that determines, which path (if any) is switched after booting the instrument. This
		RC command is equivalent to the 'Switch-On Action' in the 'General' configuration dialog of the user interface. The query
		returns the currently set switch-on action. \n
			:return: path_name: String parameter to specify the path name (see method RsOsp.Route.Path.Define.set) of the path to be switched at power-up. If you specify a path name that does not exist, the command has no effect. If you specify an empty path name string ('') , the Switch-On Action is set to None. The switch unit does not switch any path after being booted.
		"""
		response = self._core.io.query_str('CONFigure:POWerup:PATH?')
		return trim_str_response(response)

	def set_path(self, path_name: str) -> None:
		"""SCPI: CONFigure:POWerup:PATH \n
		Snippet: driver.configure.powerUp.set_path(path_name = '1') \n
		Sets or queries the switch-on action that determines, which path (if any) is switched after booting the instrument. This
		RC command is equivalent to the 'Switch-On Action' in the 'General' configuration dialog of the user interface. The query
		returns the currently set switch-on action. \n
			:param path_name: String parameter to specify the path name (see method RsOsp.Route.Path.Define.set) of the path to be switched at power-up. If you specify a path name that does not exist, the command has no effect. If you specify an empty path name string ('') , the Switch-On Action is set to None. The switch unit does not switch any path after being booted.
		"""
		param = Conversions.value_to_quoted_str(path_name)
		self._core.io.write(f'CONFigure:POWerup:PATH {param}')

	def get_reset(self) -> bool:
		"""SCPI: CONFigure:POWerup:RESet \n
		Snippet: value: bool = driver.configure.powerUp.get_reset() \n
		Sets or queries the Power Up reset condition of switch modules with latching relays. This setting determines, how
		latching relays behave after booting the switch unit. Note that this command does NOT reset the module OSP B104, which is
		designed for controlling external latching relays.
			INTRO_CMD_HELP: The following rules apply for identifying positions of latching SPDT relays: \n
			- On the relays' front plates, the positions are labeled as 2 and 1, with 2 being the default position
			- In the graphical user interface (GUI) , the positions are 0 and 1, with 0 being the default position
			- In a remote control command (SCPI) , the positions are 00 and 01, with 00 being the default value
		Hence, if you take the front-plate port labels of a latching SPDT relay, subtract 1 to get the position values that the
		software uses for this relay. The query returns the current reset condition. \n
			:return: state:
				- 1 | ON: At Power Up, the switch unit handles latching relays as follows:It sets all latching SPDT relays to the default ports labeled 2, which are represented in the software by position 0.It sets all latching SPxT relays to the open state.
				- 0 | OFF: At Power Up, the switch unit leaves all latching relays keep their previous state."""
		response = self._core.io.query_str('CONFigure:POWerup:RESet?')
		return Conversions.str_to_bool(response)

	def set_reset(self, state: bool) -> None:
		"""SCPI: CONFigure:POWerup:RESet \n
		Snippet: driver.configure.powerUp.set_reset(state = False) \n
		Sets or queries the Power Up reset condition of switch modules with latching relays. This setting determines, how
		latching relays behave after booting the switch unit. Note that this command does NOT reset the module OSP B104, which is
		designed for controlling external latching relays.
			INTRO_CMD_HELP: The following rules apply for identifying positions of latching SPDT relays: \n
			- On the relays' front plates, the positions are labeled as 2 and 1, with 2 being the default position
			- In the graphical user interface (GUI) , the positions are 0 and 1, with 0 being the default position
			- In a remote control command (SCPI) , the positions are 00 and 01, with 00 being the default value
		Hence, if you take the front-plate port labels of a latching SPDT relay, subtract 1 to get the position values that the
		software uses for this relay. The query returns the current reset condition. \n
			:param state:
				- 1 | ON: At Power Up, the switch unit handles latching relays as follows:It sets all latching SPDT relays to the default ports labeled 2, which are represented in the software by position 0.It sets all latching SPxT relays to the open state.
				- 0 | OFF: At Power Up, the switch unit leaves all latching relays keep their previous state."""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:POWerup:RESet {param}')
