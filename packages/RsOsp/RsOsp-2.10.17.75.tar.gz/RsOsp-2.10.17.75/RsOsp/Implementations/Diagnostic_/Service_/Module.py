from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Module:
	"""Module commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("module", core, parent)

	@property
	def hwInfo(self):
		"""hwInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwInfo'):
			from .Module_.HwInfo import HwInfo
			self._hwInfo = HwInfo(self._core, self._base)
		return self._hwInfo

	@property
	def temperature(self):
		"""temperature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_temperature'):
			from .Module_.Temperature import Temperature
			self._temperature = Temperature(self._core, self._base)
		return self._temperature

	@property
	def function(self):
		"""function commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_function'):
			from .Module_.Function import Function
			self._function = Function(self._core, self._base)
		return self._function
