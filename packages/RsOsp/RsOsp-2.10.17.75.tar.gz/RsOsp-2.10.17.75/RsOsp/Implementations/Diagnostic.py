from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Diagnostic:
	"""Diagnostic commands group definition. 6 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("diagnostic", core, parent)

	@property
	def service(self):
		"""service commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_service'):
			from .Diagnostic_.Service import Service
			self._service = Service(self._core, self._base)
		return self._service
