from os import PathLike

from .relation import Relation, RelType
from ... import Utils


class Image(Relation):
    def __init__(self, file: str | PathLike[str], name: str = None, style: dict = None):
        """
        Image relation class
        @param file: path to image
        @param name: filename in document
        @param style: dict with styles (e.g. width, height)
        """
        # TODO: replace name with id
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
        """ Method for converting dict style to str """
        s = ""
        for k, v in self.style.items():
            s += f"{k}:{v};"
        return s
