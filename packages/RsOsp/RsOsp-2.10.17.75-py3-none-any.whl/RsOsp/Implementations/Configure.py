from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 24 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def frame(self):
		"""frame commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_frame'):
			from .Configure_.Frame import Frame
			self._frame = Frame(self._core, self._base)
		return self._frame

	@property
	def compatible(self):
		"""compatible commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compatible'):
			from .Configure_.Compatible import Compatible
			self._compatible = Compatible(self._core, self._base)
		return self._compatible

	@property
	def virtual(self):
		"""virtual commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_virtual'):
			from .Configure_.Virtual import Virtual
			self._virtual = Virtual(self._core, self._base)
		return self._virtual

	@property
	def mainInfo(self):
		"""mainInfo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mainInfo'):
			from .Configure_.MainInfo import MainInfo
			self._mainInfo = MainInfo(self._core, self._base)
		return self._mainInfo

	@property
	def powerUp(self):
		"""powerUp commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_powerUp'):
			from .Configure_.PowerUp import PowerUp
			self._powerUp = PowerUp(self._core, self._base)
		return self._powerUp

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Configure_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def relay(self):
		"""relay commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_relay'):
			from .Configure_.Relay import Relay
			self._relay = Relay(self._core, self._base)
		return self._relay

	@property
	def lock(self):
		"""lock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lock'):
			from .Configure_.Lock import Lock
			self._lock = Lock(self._core, self._base)
		return self._lock
