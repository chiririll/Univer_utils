from os import PathLike

from .relation import Relation, RelType
from ... import Utils


class Image(Relation):
    def __init__(self, file: str | PathLike[str], name: str = None):
        fname, self.__ext = Utils.path.get_filename_and_extension(file)
        self.__name = name if name else fname

        super().__init__(
            r_type=RelType.IMAGE,
            target=f"media/{self.__name}.{self.__ext}",
            file=file,
            is_text=False
        )
