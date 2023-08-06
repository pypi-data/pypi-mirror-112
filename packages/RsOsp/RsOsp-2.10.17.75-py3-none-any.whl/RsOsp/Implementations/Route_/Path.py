from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Path:
	"""Path commands group definition. 10 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("path", core, parent)

	@property
	def define(self):
		"""define commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_define'):
			from .Path_.Define import Define
			self._define = Define(self._core, self._base)
		return self._define

	@property
	def delete(self):
		"""delete commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delete'):
			from .Path_.Delete import Delete
			self._delete = Delete(self._core, self._base)
		return self._delete

	@property
	def importPy(self):
		"""importPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_importPy'):
			from .Path_.ImportPy import ImportPy
			self._importPy = ImportPy(self._core, self._base)
		return self._importPy

	def get_catalog(self) -> List[str]:
		"""SCPI: ROUTe:PATH:CATalog \n
		Snippet: value: List[str] = driver.route.path.get_catalog() \n
		Returns a list of all currently defined path names in the internal volatile memory of the switch unit.
		The query addresses the default directory path '/home/instrument/ospdata' in the internal storage of the R&S OSP, unless
		you specify a different directory path, which is optional. \n
			:return: list_of_path_names: Comma-separated list of path names, each in quotation marks.
		"""
		response = self._core.io.query_str('ROUTe:PATH:CATalog?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)

	def get_last(self) -> str:
		"""SCPI: ROUTe:PATH:LAST \n
		Snippet: value: str = driver.route.path.get_last() \n
		Queries the name of the previously switched path. If the previous switching action was based on method RsOsp.Route.Close.
		set + channel list string (rather than a path name) , the response is <Individual Settings>. After a *RST command, the
		response is <Reset State>. In the main page of the switch unit's user interface, the line Last Switched Path (enabled by
		the 'Path Info' setting or by method RsOsp.Configure.MainInfo.path) shows the same information as the response to method
		RsOsp.Route.Path.last. \n
			:return: path_name: See method RsOsp.Route.Path.Define.set
		"""
		response = self._core.io.query_str('ROUTe:PATH:LAST?')
		return trim_str_response(response)

	def delete_all(self) -> None:
		"""SCPI: ROUTe:PATH:DELete:ALL \n
		Snippet: driver.route.path.delete_all() \n
		Deletes all previously defined paths from the switch unit’s internal volatile memory. Before you delete all paths, we
		recommend using the command method RsOsp.Route.Path.catalog to query all currently defined path names. \n
		"""
		self._core.io.write(f'ROUTe:PATH:DELete:ALL')

	def delete_all_with_opc(self) -> None:
		"""SCPI: ROUTe:PATH:DELete:ALL \n
		Snippet: driver.route.path.delete_all_with_opc() \n
		Deletes all previously defined paths from the switch unit’s internal volatile memory. Before you delete all paths, we
		recommend using the command method RsOsp.Route.Path.catalog to query all currently defined path names. \n
		Same as delete_all, but waits for the operation to complete before continuing further. Use the RsOsp.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ROUTe:PATH:DELete:ALL')

	def export(self, path_config_file: str) -> None:
		"""SCPI: ROUTe:PATH:EXPort \n
		Snippet: driver.route.path.export(path_config_file = '1') \n
		Stores a nonvolatile file in the compact flash memory of an R&S OSP by transferring it from the instrument’s internal
		volatile memory. The stored file comprises all currently defined path configurations, see method RsOsp.Route.Path.Define.
		set. All path filenames have the extension '.path'. Do not enter the extension when specifying a filename. A filename
		query does not return the extension. For example, when you save the path file 'gen-pa_1', it is saved as 'gen-pa_1.path'.
		A query returns this filename as 'gen-pa_1', only. The command MMEM:STORe:STATe is equivalent with method RsOsp.Route.
		Path.export. \n
			:param path_config_file: String parameter to specify the name of the file to be stored.
		"""
		param = Conversions.value_to_quoted_str(path_config_file)
		self._core.io.write(f'ROUTe:PATH:EXPort {param}')
