from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lock:
	"""Lock commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lock", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: CONFigure:LOCK:MODE \n
		Snippet: value: bool = driver.configure.lock.get_mode() \n
		Enables or disables the lock mode or queries this mode. \n
			:return: state:
				- 1 | ON: The switching of relays and the setting of output channels is locked.
				- 0 | OFF: Relays and output channels are not locked."""
		response = self._core.io.query_str('CONFigure:LOCK:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, state: bool) -> None:
		"""SCPI: CONFigure:LOCK:MODE \n
		Snippet: driver.configure.lock.set_mode(state = False) \n
		Enables or disables the lock mode or queries this mode. \n
			:param state:
				- 1 | ON: The switching of relays and the setting of output channels is locked.
				- 0 | OFF: Relays and output channels are not locked."""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:LOCK:MODE {param}')
