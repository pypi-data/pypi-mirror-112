from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Route:
	"""Route commands group definition. 13 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("route", core, parent)

	@property
	def close(self):
		"""close commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_close'):
			from .Route_.Close import Close
			self._close = Close(self._core, self._base)
		return self._close

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .Route_.Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._base)
		return self._attenuation

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Route_.Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def path(self):
		"""path commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_path'):
			from .Route_.Path import Path
			self._path = Path(self._core, self._base)
		return self._path
