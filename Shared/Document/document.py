import shutil
import zipfile

from jinja2 import Environment, FileSystemLoader

import Shared.Utils as utils


class Document:
    def __init__(self, path):
        # Creating empty doc file
        # TODO: Create folders
        try:
            shutil.copy("Shared/src/empty_doc/empty.doc", path)
        except PermissionError:
            self.__saved = True
            exit("Can't copy file! Please close it.")
        except FileNotFoundError:
            self.__saved = True
            exit("Empty document file or output folder does not exists!")

        self.container = zipfile.ZipFile(path, mode='a')
        self.jenv = Environment(loader=FileSystemLoader("Shared/src/parts"))
        self.jenv.globals['utils'] = utils

        # Files
        self.document = []
        self.rels = []

        # Params
        self.__r_id = 2     # free id
        self.__saved = False

    def __del__(self):
        try:
            self.save()
        except AttributeError:
            pass

    @staticmethod
    def __get_image_xml(rel_id: int, **settings):
        scale = 1     # Image scale
        size = (100, 100)

        with open('Shared/src/empty_doc/image.xml', 'r') as f:
            xml_image = f.read()

        params = {
            'rId': rel_id,
            'width': str(settings.get('size', size)[0] * scale) + 'px',
            'height': str(settings.get('size', size)[1] * scale) + 'px',
            'align': settings.get('align', "center"),
            'first_line': settings.get('first_line', 0)
        }
        for name, val in params.items():
            xml_image = xml_image.replace(f"%{name}%", str(val))

        return xml_image

    def save(self):
        if self.__saved:
            return

        with open("Shared/src/empty_doc/document.xml", encoding='UTF-8') as f:
            document = f.read().replace("%_content_%", '\n'.join(self.document))
        with open("Shared/src/empty_doc/document.xml.rels", encoding='UTF-8') as f:
            rels = f.read().replace("%_content_%", '\n'.join(self.rels))

        self.container.writestr("word/document.xml", document)
        self.container.writestr("word/_rels/document.xml.rels", rels)
        self.container.close()

        self.__saved = True
        del self

    def get_step_xml(self, step: str, **kwargs):
        # TODO: add images
        template = self.jenv.get_template(step + '.xml')
        return template.render(**kwargs)

    def add_step(self, step: str, **kwargs):
        # Adding step to document
        self.document.append(self.get_step_xml(step, **kwargs))

    def add_image(self, path) -> int:
        extension = path.split('.')[-1]
        self.container.write(path, f"word/media/{str(self.__r_id)}.{extension}")

        # Adding rel and incrementing free id
        self.rels.append(
            f"<Relationship Id=\"rId{str(self.__r_id)}\" "
            f"Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" "
            f"Target=\"media/{str(self.__r_id)}.{extension}\"/>"
        )
        self.__r_id += 1

        return self.__r_id - 1

    @staticmethod
    def txt2xml(text: str) -> str:
        """
        Contverts multi line text to word xml
        :param text: Text
        :return: Formatted xml string
        """
        xml = ""
        for line in text.split('\n'):
            xml += f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>\n"
        return xml
