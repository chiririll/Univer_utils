from abc import ABC, abstractmethod

from .executor import Executor
from ..Document import Document


class Laba(ABC):
    def __init__(self, **params):
        self.laba = {}
        self._info()

        self.executor = Executor(**params)

        self.document = Document(f"output/{self.__get_path()}_var{self.executor.variant}.doc")

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _info(self):
        pass

    def __get_path(self):
        path = ""
        path += str(self.laba.get('subject', '')) + '/'
        path += self.laba.get('name', "test")

        return path
