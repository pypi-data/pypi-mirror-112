from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MainInfo:
	"""MainInfo commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mainInfo", core, parent)

	def get_text(self) -> str:
		"""SCPI: CONFigure:MAINinfo:TEXT \n
		Snippet: value: str = driver.configure.mainInfo.get_text() \n
		Specifies or queries the text displayed as Customer Text in the Main page. This RC command is equivalent to the 'Customer
		Text' field in the 'General' configuration dialog of the user interface. \n
			:return: state: Specifies the content of the Customer Info field. Enter the content in parentheses.
		"""
		response = self._core.io.query_str('CONFigure:MAINinfo:TEXT?')
		return trim_str_response(response)

	def set_text(self, state: str) -> None:
		"""SCPI: CONFigure:MAINinfo:TEXT \n
		Snippet: driver.configure.mainInfo.set_text(state = '1') \n
		Specifies or queries the text displayed as Customer Text in the Main page. This RC command is equivalent to the 'Customer
		Text' field in the 'General' configuration dialog of the user interface. \n
			:param state: Specifies the content of the Customer Info field. Enter the content in parentheses.
		"""
		param = Conversions.value_to_quoted_str(state)
		self._core.io.write(f'CONFigure:MAINinfo:TEXT {param}')

	def get_path(self) -> bool:
		"""SCPI: CONFigure:MAINinfo:PATH \n
		Snippet: value: bool = driver.configure.mainInfo.get_path() \n
		Enables or disables displaying the Last Switched Path information in the Main page. This RC command acts equivalent to
		the Path Info checkbox in the 'General' settings dialog of the user interface. The query method RsOsp.Configure.MainInfo.
		path returns the state of this setting. The query method RsOsp.Route.Path.last returns the information on the Last
		Switched Path. \n
			:return: state:
				- 1 | ON: Displaying the Last Switched Path is enabled.
				- 0 | OFF: Displaying the Last Switched Path is disabled."""
		response = self._core.io.query_str('CONFigure:MAINinfo:PATH?')
		return Conversions.str_to_bool(response)

	def set_path(self, state: bool) -> None:
		"""SCPI: CONFigure:MAINinfo:PATH \n
		Snippet: driver.configure.mainInfo.set_path(state = False) \n
		Enables or disables displaying the Last Switched Path information in the Main page. This RC command acts equivalent to
		the Path Info checkbox in the 'General' settings dialog of the user interface. The query method RsOsp.Configure.MainInfo.
		path returns the state of this setting. The query method RsOsp.Route.Path.last returns the information on the Last
		Switched Path. \n
			:param state:
				- 1 | ON: Displaying the Last Switched Path is enabled.
				- 0 | OFF: Displaying the Last Switched Path is disabled."""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:MAINinfo:PATH {param}')
