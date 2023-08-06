from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Virtual:
	"""Virtual commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("virtual", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: CONFigure:VIRTual[:MODE] \n
		Snippet: value: bool = driver.configure.virtual.get_mode() \n
		Activates or deactivates the 'Virtual Mode'. The query returns the state of the virtual mode. \n
			:return: state:
				- 1 | ON: Activates the virtual mode.
				- 0 | OFF: Deactivates the virtual mode."""
		response = self._core.io.query_str('CONFigure:VIRTual:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, state: bool) -> None:
		"""SCPI: CONFigure:VIRTual[:MODE] \n
		Snippet: driver.configure.virtual.set_mode(state = False) \n
		Activates or deactivates the 'Virtual Mode'. The query returns the state of the virtual mode. \n
			:param state:
				- 1 | ON: Activates the virtual mode.
				- 0 | OFF: Deactivates the virtual mode."""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:VIRTual:MODE {param}')
