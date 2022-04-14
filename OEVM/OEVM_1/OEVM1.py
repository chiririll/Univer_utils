from word_parser import Document


class Laba1:
    def __init__(self, var, name, filename='out'):
        self.document = Document(f"output/{filename}.doc")

        self.var = var
        self.name = name

    def run(self):
        pass

    def to_dec(self, number: str, base: int):
        NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

        number = number.replace(',', '.')
        digits = []
        result = 0

        parts = number.split('.')
        dot_pos = number.index('.')

        for pos, d in enumerate(number.replace('.', '')):
            digit = NUMS.index(d)
            degree = dot_pos - pos - 1
            result += digit * (base ** degree)
            digits.append([digit, degree, False])
        digits[-1][2] = True    # Last digit marker

        self.document.add_step('to_dec', base=base, number=number, digits=digits, result=result)

    def name_to_ascii(self, name=None):
        if not name:
            name = ' '.join(self.name.split()[:-1])

        codes = []
        for pos, sym in enumerate(name):
            code = ord(sym) - ord('А') + 192
            if code < 192 or code > 256:
                code = 32
            codes.append((pos + 1, sym, code))

        self.document.add_step('name_to_ascii', codes=codes)
