from os import PathLike

from .relation import Relation, RelType
from ... import Utils


class Image(Relation):
    def __init__(self, file: str | PathLike[str], name: str = None, style: dict = None):
        fname, self.__ext = Utils.path.get_filename_and_extension(file)

        self.__name = name if name else fname
        self.style = style if style else {}

        super().__init__(
            r_type=RelType.IMAGE,
            target=f"media/{self.__name}.{self.__ext}",
            file=file,
            is_text=False
        )

    def get_style(self) -> str:
        s = ""
        for k, v in self.style.items():
            s += f"{k}:{v};"
        return s
