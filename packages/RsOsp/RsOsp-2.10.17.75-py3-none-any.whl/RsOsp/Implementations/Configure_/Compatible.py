from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Compatible:
	"""Compatible commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("compatible", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: CONFigure:COMPatible[:MODE] \n
		Snippet: value: bool = driver.configure.compatible.get_mode() \n
		Enables or disables backward compatibility of some currently available RC commands with the syntax of previous firmware
		versions, used for the legacy switch units of the R&S OSP1xx family: R&S OSP120, R&S OSP130 and R&S OSP150. The query
		returns the state of the compatibility mode. Note that both the current and the deprecated RC commands always are
		interpreted correctly by the firmware, independent of your compatibility settings. However, a query like 'method RsOsp.
		Route.Close.set' returns channel setting strings in the format 'F01M01' with method RsOsp.Configure.Compatible.mode = OFF
		and in the format 'F01A11' with method RsOsp.Configure.Compatible.mode = ON.
			INTRO_CMD_HELP: If the compatibility mode is enabled, the following commands are also available: \n
			- MMEM:LOAD:STATe (new: method RsOsp.Route.Path.ImportPy.value)
			- MMEM:STORe:STATe (new: method RsOsp.Route.Path.export)
			- ROUTe:MODule:CATalog?
		Note that some commands behave differently with or without the compatibility mode enabled. For example, method RsOsp.
		Route.Path.Define.set as a setting accepts both syntax versions F01M01 or F01A11. But as a query, method RsOsp.Route.Path.
		Define.set, sent without the compatibility mode enabled, returns the current syntax. On the contrary, with compatibility
		mode enabled, it returns the legacy syntax, described in section method RsOsp.Route.Path.Define.set. \n
			:return: state:
				- 1 | ON: The set of RC commands is extended as listed above for backward compatibility with R&S OSP1xx legacy switch units.
				- 0 | OFF: The firmware only accepts the standard set of RC commands. No additional commands are available to provide backward compatibility."""
		response = self._core.io.query_str('CONFigure:COMPatible:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, state: bool) -> None:
		"""SCPI: CONFigure:COMPatible[:MODE] \n
		Snippet: driver.configure.compatible.set_mode(state = False) \n
		Enables or disables backward compatibility of some currently available RC commands with the syntax of previous firmware
		versions, used for the legacy switch units of the R&S OSP1xx family: R&S OSP120, R&S OSP130 and R&S OSP150. The query
		returns the state of the compatibility mode. Note that both the current and the deprecated RC commands always are
		interpreted correctly by the firmware, independent of your compatibility settings. However, a query like 'method RsOsp.
		Route.Close.set' returns channel setting strings in the format 'F01M01' with method RsOsp.Configure.Compatible.mode = OFF
		and in the format 'F01A11' with method RsOsp.Configure.Compatible.mode = ON.
			INTRO_CMD_HELP: If the compatibility mode is enabled, the following commands are also available: \n
			- MMEM:LOAD:STATe (new: method RsOsp.Route.Path.ImportPy.value)
			- MMEM:STORe:STATe (new: method RsOsp.Route.Path.export)
			- ROUTe:MODule:CATalog?
		Note that some commands behave differently with or without the compatibility mode enabled. For example, method RsOsp.
		Route.Path.Define.set as a setting accepts both syntax versions F01M01 or F01A11. But as a query, method RsOsp.Route.Path.
		Define.set, sent without the compatibility mode enabled, returns the current syntax. On the contrary, with compatibility
		mode enabled, it returns the legacy syntax, described in section method RsOsp.Route.Path.Define.set. \n
			:param state:
				- 1 | ON: The set of RC commands is extended as listed above for backward compatibility with R&S OSP1xx legacy switch units.
				- 0 | OFF: The firmware only accepts the standard set of RC commands. No additional commands are available to provide backward compatibility."""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:COMPatible:MODE {param}')
