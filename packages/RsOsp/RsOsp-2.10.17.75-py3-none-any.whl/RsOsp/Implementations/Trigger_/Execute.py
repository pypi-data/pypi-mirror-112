from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self, type_py: enums.TriggerExecType = None) -> None:
		"""SCPI: TRIGger:EXECute \n
		Snippet: driver.trigger.execute.set(type_py = enums.TriggerExecType.RESet) \n
		Sends a software trigger event or resets the trigger sequence. \n
			:param type_py:
				- TRIGger: TRIG:EXEC TRIG sends software trigger event, equivalent with the 'Manual Trigger'.
				- RESet: TRIG:EXEC RES resets the sequence of the 'Sequenced' trigger."""
		param = ''
		if type_py:
			param = Conversions.enum_scalar_to_str(type_py, enums.TriggerExecType)
		self._core.io.write(f'TRIGger:EXECute {param}'.strip())
