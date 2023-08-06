from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restore:
	"""Restore commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restore", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Restore_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def delete(self, restore_file_to_delete: str) -> None:
		"""SCPI: CONFigure:ALL:RESTore:DELete \n
		Snippet: driver.configure.all.restore.delete(restore_file_to_delete = '1') \n
		Deletes a selected settings backup file from the switch unit’s internal flash memory. Use the command method RsOsp.
		Configure.All.Restore.Catalog.get_ to query the list of available backup files. All configuration filenames have the
		extension '.backup'. Do not enter the extension when specifying a filename. A filename query does not return the
		extension. For example, when you save the 'Interconnection' definition file 'settings-2018-10-25', it is saved as
		'settings-2018-10-25.backup'. A query returns this filename as 'settings-2018-10-25', only. \n
			:param restore_file_to_delete: String parameter to select the backup file to be deleted. If this file does not exist, a SCPI error is generated. You can query the error with SYST:ERR?. The result can be, for example: -200,'Execution error;File does not exist.,CONFigure:ALL:RESTore:DELete ''backup1'''
		"""
		param = Conversions.value_to_quoted_str(restore_file_to_delete)
		self._core.io.write(f'CONFigure:ALL:RESTore:DELete {param}')

	def delete_all(self, path_information: str = None) -> None:
		"""SCPI: CONFigure:ALL:RESTore:DELete:ALL \n
		Snippet: driver.configure.all.restore.delete_all(path_information = '1') \n
		Risk of losing settings: Removes all settings backup files from the switch unit’s internal memory or from a removable
		flash memory. Before you delete all settings backup files, we recommend using the command method RsOsp.Configure.All.
		Restore.Catalog.get_ to query the currently defined settings backup files. All configuration filenames have the extension
		'.backup'. Do not enter the extension when specifying a filename. A filename query does not return the extension.
		For example, when you save the 'Interconnection' definition file 'settings-2018-10-25', it is saved as
		'settings-2018-10-25.backup'. A query returns this filename as 'settings-2018-10-25', only. \n
			:param path_information: No help available
		"""
		param = ''
		if path_information:
			param = Conversions.value_to_quoted_str(path_information)
		self._core.io.write(f'CONFigure:ALL:RESTore:DELete:ALL {param}'.strip())

	def set_value(self, restore_file_to_restore: str) -> None:
		"""SCPI: CONFigure:ALL:RESTore \n
		Snippet: driver.configure.all.restore.set_value(restore_file_to_restore = '1') \n
		Loads a file previously saved as a backup of all settings (see method RsOsp.Configure.All.backup) and uses it to
		overwrite the current settings. All configuration filenames have the extension '.backup'. Do not enter the extension when
		specifying a filename. A filename query does not return the extension. For example, when you save the 'Interconnection'
		definition file 'settings-2018-10-25', it is saved as 'settings-2018-10-25.backup'. A query returns this filename as
		'settings-2018-10-25', only. Risk of losing settings: This command overwrites all current settings in the switch unit’s
		internal memory with the settings in the loaded file. To avoid losing current settings, consider saving these settings by
		method RsOsp.Configure.All.backup, before you send the restore command. \n
			:param restore_file_to_restore: String parameter to select the backup file to be restored. The user interface ('WebGUI') shows only files that were saved in the default directory, hence, without specifying an additional file path.
		"""
		param = Conversions.value_to_quoted_str(restore_file_to_restore)
		self._core.io.write(f'CONFigure:ALL:RESTore {param}')
