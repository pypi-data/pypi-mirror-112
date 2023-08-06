from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	def get_level(self) -> float:
		"""SCPI: TRIGger:SIGNal:LEVel \n
		Snippet: value: float = driver.trigger.signal.get_level() \n
		Sets or queries the voltage level, which defines the threshold for a trigger event. The level setting is not influenced
		by reset commands. \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('TRIGger:SIGNal:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: TRIGger:SIGNal:LEVel \n
		Snippet: driver.trigger.signal.set_level(level = 1.0) \n
		Sets or queries the voltage level, which defines the threshold for a trigger event. The level setting is not influenced
		by reset commands. \n
			:param level: Specifies the voltage level. Factory default is 2.5 V.
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'TRIGger:SIGNal:LEVel {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.TriggerSlope:
		"""SCPI: TRIGger:SIGNal:SLOPe \n
		Snippet: value: enums.TriggerSlope = driver.trigger.signal.get_slope() \n
		Sets or queries, which kind of threshold transition is interpreted as a trigger event. For the threshold level, see
		method RsOsp.Trigger.Signal.level. \n
			:return: slope:
				- POSitive: Defines interpreting a positive (low-to-high) transition of the threshold as a trigger event.
				- NEGative: Defines interpreting a negative (high-to-low) transition of the threshold as a trigger event.
				- BOTH: Defines interpreting a positive or a negative transition of the threshold as a trigger event.Equivalent with Any in the user interface ('WebGUI') ."""
		response = self._core.io.query_str('TRIGger:SIGNal:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSlope)

	def set_slope(self, slope: enums.TriggerSlope) -> None:
		"""SCPI: TRIGger:SIGNal:SLOPe \n
		Snippet: driver.trigger.signal.set_slope(slope = enums.TriggerSlope.BOTH) \n
		Sets or queries, which kind of threshold transition is interpreted as a trigger event. For the threshold level, see
		method RsOsp.Trigger.Signal.level. \n
			:param slope:
				- POSitive: Defines interpreting a positive (low-to-high) transition of the threshold as a trigger event.
				- NEGative: Defines interpreting a negative (high-to-low) transition of the threshold as a trigger event.
				- BOTH: Defines interpreting a positive or a negative transition of the threshold as a trigger event.Equivalent with Any in the user interface ('WebGUI') ."""
		param = Conversions.enum_scalar_to_str(slope, enums.TriggerSlope)
		self._core.io.write(f'TRIGger:SIGNal:SLOPe {param}')

	def get_termination(self) -> float:
		"""SCPI: TRIGger:SIGNal:TERMination \n
		Snippet: value: float = driver.trigger.signal.get_termination() \n
		Sets or queries the type of termination of the trigger signal cable. \n
			:return: termination: No help available
		"""
		response = self._core.io.query_str('TRIGger:SIGNal:TERMination?')
		return Conversions.str_to_float(response)

	def set_termination(self, termination: float) -> None:
		"""SCPI: TRIGger:SIGNal:TERMination \n
		Snippet: driver.trigger.signal.set_termination(termination = 1.0) \n
		Sets or queries the type of termination of the trigger signal cable. \n
			:param termination:
				- 50OHM: Sets the termination to 50 Ohm.Also accepted parameter syntax: '50' or '50 ohm' (a blank and all capital/small letters are ignored) .
				- HIGH: Sets the termination to High, equivalent with High Impedance in the user interface ('WebGUI') .Also accepted parameter syntax: 'high' (capital/small letters are ignored) ."""
		param = Conversions.decimal_value_to_str(termination)
		self._core.io.write(f'TRIGger:SIGNal:TERMination {param}')
