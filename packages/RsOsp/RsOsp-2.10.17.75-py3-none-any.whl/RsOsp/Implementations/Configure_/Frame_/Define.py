from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Define:
	"""Define commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("define", core, parent)

	def set(self, frame_id: str, configured_address: str) -> None:
		"""SCPI: CONFigure:FRAMe[:DEFine] \n
		Snippet: driver.configure.frame.define.set(frame_id = r1, configured_address = '1') \n
		Defines how an existing secondary switch unit is addressed via LAN by the primary switch unit. To do so, the command
		selects a secondary switch unit by its IP address or hostname and allows you to set the frame ID of this secondary switch
		unit in the 'Interconnection' configuration of the primary switch unit. Note that this command does not change the
		network settings or IP address of the primary or secondary device. It only defines the ID, by which a primary device
		addresses a secondary device. The query returns the IP address of the secondary switch unit with the specified frame ID.
		To query the full list of existing secondary switch units, use the command method RsOsp.Configure.Frame.catalog.
		Note that you can add or insert new secondary switch units with separate commands. The current configuration is always
		saved automatically to the flash memory during the shutdown procedure and loaded at startup into the volatile memory. To
		save a specific configuration of all frames to a separate file on the switch unit's compact flash memory, use the command
		method RsOsp.Configure.Frame.export. \n
			:param frame_id: Selects the frame ID Fxx of the secondary switch unit that you wish to modify, starting with F02 (note that the 1st secondary switch unit is the 2nd frame) . Use the frame ID without quotation marks. In a setting, if you use F01 or a frame ID, for which no secondary switch unit is defined, a SCPI error is generated. In a query, if you use F01, an empty response is returned. If you use a frame ID, for which no secondary switch unit is defined, a SCPI error is generated.
			:param configured_address: Specifies the IP address or hostname, at which the secondary switch unit (selected by the frameId) is available via LAN. Use the address or hostname in quotation marks.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('frame_id', frame_id, DataType.RawString), ArgSingle('configured_address', configured_address, DataType.String))
		self._core.io.write(f'CONFigure:FRAMe:DEFine {param}'.rstrip())

	def get(self, frame_id: str) -> str:
		"""SCPI: CONFigure:FRAMe[:DEFine] \n
		Snippet: value: str = driver.configure.frame.define.get(frame_id = r1) \n
		Defines how an existing secondary switch unit is addressed via LAN by the primary switch unit. To do so, the command
		selects a secondary switch unit by its IP address or hostname and allows you to set the frame ID of this secondary switch
		unit in the 'Interconnection' configuration of the primary switch unit. Note that this command does not change the
		network settings or IP address of the primary or secondary device. It only defines the ID, by which a primary device
		addresses a secondary device. The query returns the IP address of the secondary switch unit with the specified frame ID.
		To query the full list of existing secondary switch units, use the command method RsOsp.Configure.Frame.catalog.
		Note that you can add or insert new secondary switch units with separate commands. The current configuration is always
		saved automatically to the flash memory during the shutdown procedure and loaded at startup into the volatile memory. To
		save a specific configuration of all frames to a separate file on the switch unit's compact flash memory, use the command
		method RsOsp.Configure.Frame.export. \n
			:param frame_id: Selects the frame ID Fxx of the secondary switch unit that you wish to modify, starting with F02 (note that the 1st secondary switch unit is the 2nd frame) . Use the frame ID without quotation marks. In a setting, if you use F01 or a frame ID, for which no secondary switch unit is defined, a SCPI error is generated. In a query, if you use F01, an empty response is returned. If you use a frame ID, for which no secondary switch unit is defined, a SCPI error is generated.
			:return: configured_address: Specifies the IP address or hostname, at which the secondary switch unit (selected by the frameId) is available via LAN. Use the address or hostname in quotation marks."""
		param = Conversions.value_to_str(frame_id)
		response = self._core.io.query_str(f'CONFigure:FRAMe:DEFine? {param}')
		return trim_str_response(response)
