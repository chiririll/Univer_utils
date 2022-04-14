from enum import Enum
from os import PathLike


class RelType(Enum):
    STYLE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"
    )
    IMAGE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
        None
    )
    FOOTER = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"
    )


class Relation:
    def __init__(self, r_type: RelType, target: str, file: str | PathLike[str], r_id: int = 0):
        self.id = r_id
        self.type, self.override = r_type.value
        self.target = target
        self.file = file
