from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


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

	def delete(self, slave_config_file: str) -> None:
		"""SCPI: CONFigure:FRAMe:IMPort:DELete \n
		Snippet: driver.configure.frame.importPy.delete(slave_config_file = '1') \n
		Risk of losing settings: Removes the specified interconnection configuration file from the primary switch unit’s compact
		flash memory. All secondary switch unit configuration filenames have the extension '.iconn'. Do not enter the extension
		when specifying a filename. A filename query does not return the extension. For example, when you save the
		interconnection configuration file 'subunit1', it is saved as 'subunit1.iconn'. A query returns this filename as
		'subunit1', only. Legacy file extensions are still supported. \n
			:param slave_config_file: String parameter to specify the name of the file to be deleted. If this file does not exist, a SCPI error is generated. You can query the error with SYST:ERR?. The result can be, for example: -200,'Execution error;File does not exist.,CONF:FRAM:IMP:DEL ''setup3frameconfigs'''
		"""
		param = Conversions.value_to_quoted_str(slave_config_file)
		self._core.io.write(f'CONFigure:FRAMe:IMPort:DELete {param}')

	def delete_all(self, path_information: str = None) -> None:
		"""SCPI: CONFigure:FRAMe:IMPort:DELete:ALL \n
		Snippet: driver.configure.frame.importPy.delete_all(path_information = '1') \n
		Risk of losing settings: Removes all interconnection configuration files from the primary switch unit’s compact flash
		memory. Before you delete all secondary switch unit configuration files, we recommend using the command method RsOsp.
		Configure.Frame.ImportPy.Catalog.get_ to query all currently defined interconnection configuration files. All secondary
		switch unit configuration filenames have the extension '.iconn'. Do not enter the extension when specifying a filename. A
		filename query does not return the extension. For example, when you save the interconnection configuration file
		'subunit1', it is saved as 'subunit1.iconn'. A query returns this filename as 'subunit1', only. Legacy file extensions
		are still supported. \n
			:param path_information: No help available
		"""
		param = ''
		if path_information:
			param = Conversions.value_to_quoted_str(path_information)
		self._core.io.write(f'CONFigure:FRAMe:IMPort:DELete:ALL {param}'.strip())

	def set_value(self, slave_config_file: str) -> None:
		"""SCPI: CONFigure:FRAMe:IMPort \n
		Snippet: driver.configure.frame.importPy.set_value(slave_config_file = '1') \n
		Loads a secondary devices configuration file from the compact flash memory of your primary switch unit into its internal
		volatile memory. As a prerequisite, you must have exported such a file in advance, see method RsOsp.Configure.Frame.
		export. All secondary switch unit configuration filenames have the extension '.iconn'. Do not enter the extension when
		specifying a filename. A filename query does not return the extension. For example, when you save the interconnection
		configuration file 'subunit1', it is saved as 'subunit1.iconn'. A query returns this filename as 'subunit1', only. Legacy
		file extensions are still supported. Risk of losing settings: Note that this command overwrites the secondary switch
		units in the current frames configuration in the primary switch unit’s internal memory with the secondary switch units
		configuration in the loaded file. To avoid losing a current secondary switch units configuration, consider saving this
		configuration by method RsOsp.Configure.Frame.export, before you send the import command. \n
			:param slave_config_file: String parameter to specify the name of the file to be loaded.
		"""
		param = Conversions.value_to_quoted_str(slave_config_file)
		self._core.io.write(f'CONFigure:FRAMe:IMPort {param}')
