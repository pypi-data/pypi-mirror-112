from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 17 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def signal(self):
		"""signal commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_signal'):
			from .Trigger_.Signal import Signal
			self._signal = Signal(self._core, self._base)
		return self._signal

	@property
	def sequence(self):
		"""sequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Trigger_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Trigger_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_count'):
			from .Trigger_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def importPy(self):
		"""importPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_importPy'):
			from .Trigger_.ImportPy import ImportPy
			self._importPy = ImportPy(self._core, self._base)
		return self._importPy

	def get_state(self) -> bool:
		"""SCPI: TRIGger:STATe \n
		Snippet: value: bool = driver.trigger.get_state() \n
		Sets or queries the activation state of the trigger functionality. \n
			:return: activation_state: No help available
		"""
		response = self._core.io.query_str('TRIGger:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, activation_state: bool) -> None:
		"""SCPI: TRIGger:STATe \n
		Snippet: driver.trigger.set_state(activation_state = False) \n
		Sets or queries the activation state of the trigger functionality. \n
			:param activation_state:
				- OFF: Deactivates the trigger functionality. The command does not accept '0' instead of 'OFF'.
				- ON: Activates the trigger functionality. The command does not accept '1' instead of 'ON'."""
		param = Conversions.bool_to_str(activation_state)
		self._core.io.write(f'TRIGger:STATe {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.TriggerType:
		"""SCPI: TRIGger:TYPE \n
		Snippet: value: enums.TriggerType = driver.trigger.get_type_py() \n
		Selects or queries the trigger type. \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('TRIGger:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerType)

	def set_type_py(self, type_py: enums.TriggerType) -> None:
		"""SCPI: TRIGger:TYPE \n
		Snippet: driver.trigger.set_type_py(type_py = enums.TriggerType.ADDRessed) \n
		Selects or queries the trigger type. \n
			:param type_py:
				- SINGle: Selects the trigger type Single.
				- TOGGle: Selects the trigger type Toggle A-B.
				- SEQuenced: Selects the trigger type Sequenced.
				- ADDRessed: Selects the trigger type Addressed."""
		param = Conversions.enum_scalar_to_str(type_py, enums.TriggerType)
		self._core.io.write(f'TRIGger:TYPE {param}')

	def get_index(self) -> int:
		"""SCPI: TRIGger:INDex \n
		Snippet: value: int = driver.trigger.get_index() \n
		Queries the trigger index, which is the number of the currently triggered path in the trigger types described below.
			INTRO_CMD_HELP: The returned component information consists of: \n
			- 'Toggle A-B', the index has the following meaning:
			INTRO_CMD_HELP: The returned component information consists of: \n
			- -1 = no trigger event yet, method RsOsp.Trigger.Count.value = 0
			- 0 = Path A
			- 1 = Path B
			- 'Sequenced', the index has the following meaning:
			INTRO_CMD_HELP: The returned component information consists of: \n
			- -1 = no trigger event yet, method RsOsp.Trigger.Count.value = 0
			- 0 = Path 0
			- 1 = Path 1
			- 2 = Path 2
			- ...
			- 15 = Path 15  \n
			:return: index: No help available
		"""
		response = self._core.io.query_str('TRIGger:INDex?')
		return Conversions.str_to_int(response)

	def export(self, trigger_config_file: str) -> None:
		"""SCPI: TRIGger:EXPort \n
		Snippet: driver.trigger.export(trigger_config_file = '1') \n
		Stores the currently defined trigger configuration as a nonvolatile file in the compact flash memory of your primary
		switch unit. \n
			:param trigger_config_file: String parameter to specify the name of the file to be stored.
		"""
		param = Conversions.value_to_quoted_str(trigger_config_file)
		self._core.io.write(f'TRIGger:EXPort {param}')
