from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, frame_id: str, configured_address: str) -> None:
		"""SCPI: CONFigure:FRAMe:INSert \n
		Snippet: driver.configure.frame.insert.set(frame_id = r1, configured_address = '1') \n
		Inserts an entry for a secondary switch unit ahead of an existing entry in the list of frame IDs in the switch unit’s
		internal volatile memory. \n
			:param frame_id: Specifies the frame ID Fxx, at which the new secondary switch unit is to be inserted. The lowest accepted frame ID is F02. Existing frame IDs from this frame ID on are automatically renumbered (incremented by 1) . If the specified frame ID is not yet defined, a SCPI error is generated.
			:param configured_address: Specifies the IP address or the hostname of the secondary switch unit that you want to insert.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('frame_id', frame_id, DataType.RawString), ArgSingle('configured_address', configured_address, DataType.String))
		self._core.io.write(f'CONFigure:FRAMe:INSert {param}'.rstrip())
