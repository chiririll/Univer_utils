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

        word_params = params.get('word_params', {})

        word_params['jinja_globals'] = {
            'subject': self.subject,
            'laba': self.laba,
            'executor': self.executor,
            **word_params.get('jinja_globals', {})
        }

        self.document = Document(doc_path, **word_params)

    @abstractmethod
    def run(self):
        pass

    def __get_path(self):
        path = ""
        path += str(self.laba.get('subject', '')) + '/'
        path += self.laba.get('name', "test")

        return path
