from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delete:
	"""Delete commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delete", core, parent)

	def set_name(self, path_name: str) -> None:
		"""SCPI: ROUTe:PATH:DELete[:NAME] \n
		Snippet: driver.route.path.delete.set_name(path_name = '1') \n
		Deletes the path specified by the <path name> parameter from the switch unit’s internal volatile memory. If this path
		does not exist, the command has no effect. \n
			:param path_name: See method RsOsp.Route.Path.Define.set.
		"""
		param = Conversions.value_to_quoted_str(path_name)
		self._core.io.write(f'ROUTe:PATH:DELete:NAME {param}')
