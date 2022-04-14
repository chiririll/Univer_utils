import datetime
from io import BytesIO
from os import PathLike
from zipfile import ZipFile

import jinja2

from .relation import Relation, RelType
from .. import Utils


class Document:

    EMPTY_DOC_FOLDER = "Shared/src/empty_doc/"
    STYLES_FOLDER = "Shared/src/styles/"
    SHARED_TEMPLATES = [
        "Shared/src/parts/",
        EMPTY_DOC_FOLDER
    ]

    def __init__(self, container: str | PathLike[str] | BytesIO, **params):
        def create_jinja_env() -> jinja2.Environment:
            global_vars = {
                'date': datetime.date.today(),
                **params.get('jinja_globals', {})
            }

            folders = self.SHARED_TEMPLATES
            if params.get('parts_folder'):
                folders.append(params.get('parts_folder'))

            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(folders)
            )

            for k, v in global_vars.items():
                env.globals[k] = v

            return env

        self.__saved = False

        self.zip = ZipFile(container, 'w')
        self.jenv = create_jinja_env()

        self.content = []
        self.rels = []

        # Adding style
        self.add_relation(
            Relation(RelType.STYLE, "styles.xml", self.STYLES_FOLDER + params.get('style', 'default') + ".xml")
        )

    def __del__(self):
        try:
            if not self.__saved:
                self.save()
        except AttributeError:
            pass

    def add_relation(self, relation: Relation):
        relation.id = len(self.rels) + 1
        self.rels.append(relation)
        return relation.id

    def save(self):
        context = {
            'rels': self.rels,
            'content': self.content,
        }

        # Adding static files
        for file in Utils.path.walk(self.EMPTY_DOC_FOLDER):
            template = self.jenv.get_template(file)
            self.zip.writestr(file, template.render(**context))

        # Adding relations
        for rel in self.rels:
            self.zip.write(rel.file, 'word/' + rel.target)

        self.zip.close()

        self.__saved = True
        del self

    def add_paragraph(self, text: str):
        lines = []
        for line in text.split('\n'):
            lines.append(f"<w:r><w:t>{line}</w:t></w:r>")
        lines = '\n'.join(lines)
        self.content.append(f"<w:p>{lines}</w:p>")

    def add_step(self, step_name: str, **context):
        step = self.jenv.get_template(step_name + '.xml')
        self.content.append(step.render(**context))
