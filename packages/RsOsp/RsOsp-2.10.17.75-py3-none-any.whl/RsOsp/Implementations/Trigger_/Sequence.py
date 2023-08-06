from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	@property
	def define(self):
		"""define commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_define'):
			from .Sequence_.Define import Define
			self._define = Define(self._core, self._base)
		return self._define
