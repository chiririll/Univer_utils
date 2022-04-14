from enum import Enum
from io import BytesIO
from os import PathLike


class RelType(Enum):
    STYLE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"


class Relation:
    def __init__(self, r_type: RelType, target: str, file: str | PathLike[str] | BytesIO, r_id: int = 0):
        self.id = r_id
        self.type = r_type.value
        self.target = target
        self.file = file
