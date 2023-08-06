from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImportPy:
	"""ImportPy commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("importPy", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .ImportPy_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def delete(self, trigger_config_file: str) -> None:
		"""SCPI: TRIGger:IMPort:DELete \n
		Snippet: driver.trigger.importPy.delete(trigger_config_file = '1') \n
		Risk of losing settings: Removes the specified trigger configuration file from the primary switch unit’s compact flash
		memory. All trigger configuration filenames have the extension '.trigger'. Do not enter the extension when specifying a
		filename. A filename query does not return the extension. For example, when you save the trigger configuration file
		'trg42', it is saved as 'trg42.trigger'. A query returns this filename as 'trg42', only. \n
			:param trigger_config_file: String parameter to specify the name of the file to be deleted. If this file does not exist, a SCPI error is generated. You can query the error with SYST:ERR?. The result can be, for example: -200,'Execution error;File does not exist.,TRIG:IMP:DEL ''sequencedtrig2'''
		"""
		param = Conversions.value_to_quoted_str(trigger_config_file)
		self._core.io.write(f'TRIGger:IMPort:DELete {param}')

	def delete_all(self, path_information: str = None) -> None:
		"""SCPI: TRIGger:IMPort:DELete:ALL \n
		Snippet: driver.trigger.importPy.delete_all(path_information = '1') \n
		Risk of losing settings: Removes all trigger configuration files from the primary switch unit’s compact flash memory.
		Before you delete all trigger configuration files, we recommend using the command method RsOsp.Trigger.ImportPy.Catalog.
		get_ to query all currently stored trigger configuration files. All trigger configuration filenames have the extension '.
		trigger'. Do not enter the extension when specifying a filename. A filename query does not return the extension.
		For example, when you save the trigger configuration file 'trg42', it is saved as 'trg42.trigger'. A query returns this
		filename as 'trg42', only. \n
			:param path_information: No help available
		"""
		param = ''
		if path_information:
			param = Conversions.value_to_quoted_str(path_information)
		self._core.io.write(f'TRIGger:IMPort:DELete:ALL {param}'.strip())

	def set_value(self, import_filename: str) -> None:
		"""SCPI: TRIGger:IMPort \n
		Snippet: driver.trigger.importPy.set_value(import_filename = '1') \n
		Loads a trigger configuration file from the compact flash memory of your primary switch unit into its internal volatile
		memory. As a prerequisite, you must have exported such a file in advance, see method RsOsp.Trigger.export. All trigger
		configuration filenames have the extension '.trigger'. Do not enter the extension when specifying a filename. A filename
		query does not return the extension. For example, when you save the trigger configuration file 'trg42', it is saved as
		'trg42.trigger'. A query returns this filename as 'trg42', only. Risk of losing settings: Note that this command
		overwrites the current trigger configuration in the primary switch unit’s internal memory with the trigger configuration
		in the loaded file. To avoid losing a current trigger configuration, consider saving this configuration by method RsOsp.
		Trigger.export, before you send the import command. \n
			:param import_filename: String parameter to specify the name of the file to be stored.
		"""
		param = Conversions.value_to_quoted_str(import_filename)
		self._core.io.write(f'TRIGger:IMPort {param}')
