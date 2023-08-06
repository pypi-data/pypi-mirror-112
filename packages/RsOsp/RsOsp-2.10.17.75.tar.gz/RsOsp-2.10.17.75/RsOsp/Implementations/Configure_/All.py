from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 5 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	@property
	def restore(self):
		"""restore commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_restore'):
			from .All_.Restore import Restore
			self._restore = Restore(self._core, self._base)
		return self._restore

	def set_backup(self, filename_for_backup: str) -> None:
		"""SCPI: CONFigure:ALL:BACKup \n
		Snippet: driver.configure.all.set_backup(filename_for_backup = '1') \n
			INTRO_CMD_HELP: Saves all configuration settings to a backup file. These settings comprise the following: \n
			- General configuration
			- Network settings
			- Trigger configuration (optional)
			- Interconnection configuration
			- Virtual configuration
		All configuration filenames have the extension '.backup'. Do not enter the extension when specifying a filename.
		A filename query does not return the extension. For example, when you save the 'Interconnection' definition file
		'settings-2018-10-25', it is saved as 'settings-2018-10-25.backup'.
		A query returns this filename as 'settings-2018-10-25', only. \n
			:param filename_for_backup: String parameter to specify the filename for the backup.
		"""
		param = Conversions.value_to_quoted_str(filename_for_backup)
		self._core.io.write(f'CONFigure:ALL:BACKup {param}')
