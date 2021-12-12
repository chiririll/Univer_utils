import shutil
import zipfile


class Document:
    def __init__(self, path):
        # Creating empty doc file
        shutil.copy("src/empty_doc/Empty.doc", path)
        self.container = zipfile.ZipFile(path, mode='a')

        # Files
        self.document = []
        self.rels = []

        # Params
        self.__r_id = 2     # free id
        self.__shapetype_added = False
        self.__saved = False

    def __del__(self):
        self.save()

    def __get_image_xml(self, rel_id: int, size: tuple = ('467.25pt', '300pt')):
        path = f"src/empty_doc/parts/"
        scale = 0.63     # Image scale

        if self.__shapetype_added:
            path += "image_min.xml"
        else:
            path += "image.xml"
            self.__shapetype_added = True

        with open(path) as f:
            xml_image = f.read()

        params = {
            'rId': str(rel_id),
            'width': str(size[0] * scale) + 'px',
            'height': str(size[1] * scale) + 'px'
        }
        for name, val in params.items():
            xml_image = xml_image.replace(f"%{name}%", val)

        return xml_image

    def save(self):
        if self.__saved:
            return

        with open("src/empty_doc/document.xml", encoding='UTF-8') as f:
            document = f.read().replace("%_content_%", '\n'.join(self.document))
        with open("src/empty_doc/document.xml.rels", encoding='UTF-8') as f:
            rels = f.read().replace("%_content_%", '\n'.join(self.rels))

        self.container.writestr("word/document.xml", document)
        self.container.writestr("word/_rels/document.xml.rels", rels)
        self.container.close()

        self.__saved = True
        del self

    def add_step(self, step: str, **kwargs):
        # Reading step xml file
        with open(f"src/empty_doc/steps/{step}.xml", 'r', encoding='UTF-8') as f:
            step_xml = f.read()

        # Replacing markers
        for name, val in kwargs.items():
            if "image" in name:
                img_id = self.add_image(val['path'])
                val = self.__get_image_xml(img_id, val['size'])

            step_xml = step_xml.replace(f"%{name}%", str(val))

        # Adding step to document
        self.document.append(step_xml)

    def add_image(self, path) -> int:
        self.container.write(path, f"word/media/{str(self.__r_id)}.png")

        # Adding rel and incrementing free id
        self.rels.append(
            f"<Relationship Id=\"rId{str(self.__r_id)}\" "
            f"Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" "
            f"Target=\"media/{str(self.__r_id)}.png\"/>"
        )
        self.__r_id += 1

        return self.__r_id - 1
