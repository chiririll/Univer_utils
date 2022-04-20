from enum import Enum
from os import PathLike


class RelType(Enum):
    """ Relation types (type link, overridable format) """
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
    """ Base class for relation """
    def __init__(self,
                 r_type: RelType,
                 target: str,
                 file: str | PathLike[str],
                 is_text: bool = False,
                 context: dict = None,
                 r_id: int = 0
                 ):
        self.__id = r_id
        self.__type = r_type
        self.__target = target
        self.__file = file
        self.__is_text = is_text
        self.__context = context

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, r_id: int) -> None:
        self.__id = r_id

    @property
    def type(self) -> str:
        return self.__type.value[0]

    @type.setter
    def type(self, r_type: RelType) -> None:
        pass

    @property
    def override(self) -> str:
        return self.__type.value[1]

    @property
    def target(self) -> str:
        return self.__target

    @target.setter
    def target(self, target: str) -> None:
        self.__target = target

    @property
    def file(self) -> str | PathLike[str]:
        return self.__file

    @file.setter
    def file(self, file: str | PathLike[str]):
        pass

    @property
    def is_text(self) -> bool:
        return self.__is_text

    @is_text.setter
    def is_text(self, is_text: bool) -> None:
        pass

    @property
    def context(self) -> dict:
        return self.__context

    @context.setter
    def context(self, context: dict) -> None:
        self.__context = context
