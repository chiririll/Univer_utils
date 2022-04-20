from os import PathLike

from .relation import Relation, RelType


class Xml(Relation):
    def __init__(self, r_type: RelType, target: str, file: str | PathLike[str], **context):
        """
        Simple xml relation
        @param r_type: Relation type
        @param target: Target file in document
        @param file: Path to file
        @param context: Params for jinja
        """
        super().__init__(
            r_type=r_type,
            target=target,
            file=file,
            is_text=True,
            context=context
        )

    @property
    def content(self) -> str:
        with open(self.file, 'r', encoding="UTF-8") as f:
            return f.read()
