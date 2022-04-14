from abc import ABC, abstractmethod

from .executor import Executor
from .. import Utils
from ..Document import Document


class Laba(ABC):

    laba = {
        'name': "test",
        'subject': None
    }

    subject = {
        'title': "Test subject",
        'teacher': "Ivanov Ivan Ivanovich"
    }

    def __init__(self, **params):

        self.executor = Executor(**params)

        doc_path = f"output/{self.__get_path()}_v{self.executor.variant}.doc"
        Utils.path.create_folders(doc_path)
        self.document = Document(doc_path, **params.get('word_params', {}))

    @abstractmethod
    def run(self):
        pass

    def __get_path(self):
        path = ""
        path += str(self.laba.get('subject', '')) + '/'
        path += self.laba.get('name', "test")

        return path
