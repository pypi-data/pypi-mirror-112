from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Module:
	"""Module commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("module", core, parent)

	@property
	def interlock(self):
		"""interlock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interlock'):
			from .Module_.Interlock import Interlock
			self._interlock = Interlock(self._core, self._base)
		return self._interlock
