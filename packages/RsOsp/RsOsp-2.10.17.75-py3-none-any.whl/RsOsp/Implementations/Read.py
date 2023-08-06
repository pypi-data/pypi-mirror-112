from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Read:
	"""Read commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("read", core, parent)

	@property
	def io(self):
		"""io commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_io'):
			from .Read_.Io import Io
			self._io = Io(self._core, self._base)
		return self._io

	@property
	def module(self):
		"""module commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_module'):
			from .Read_.Module import Module
			self._module = Module(self._core, self._base)
		return self._module

	@property
	def relay(self):
		"""relay commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_relay'):
			from .Read_.Relay import Relay
			self._relay = Relay(self._core, self._base)
		return self._relay
