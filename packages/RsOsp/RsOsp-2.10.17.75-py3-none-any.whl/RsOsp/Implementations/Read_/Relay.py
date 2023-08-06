from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relay:
	"""Relay commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("relay", core, parent)

	@property
	def operations(self):
		"""operations commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_operations'):
			from .Relay_.Operations import Operations
			self._operations = Operations(self._core, self._base)
		return self._operations
