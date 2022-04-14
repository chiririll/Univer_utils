class Pattern:
    def __init__(self, pattern: str = None):
        if pattern is None:
            pattern = 'SNP'

        self.__positions = []
        self.update_pattern(pattern)

    def update_pattern(self, pattern: str):
        self.__positions.clear()
        for pos in pattern.upper():
            if pos == 'S' and 'S' not in self.__positions:
                self.__positions.append('S')
            elif pos == 'N' and 'N' not in self.__positions:
                self.__positions.append('N')
            elif pos == 'P' and 'P' not in self.__positions:
                self.__positions.append('P')
            else:
                raise ValueError(f'Pattern "{pattern}" is not a valid pattern!')

    def get_list(self, surname: str = '', name: str = '', patronymic: str = '') -> list:
        items = {'S': surname, 'N': name, 'P': patronymic}
        return list(map(lambda pos: items[pos], self.__positions))

    def get_str(self, surname: str = '', name: str = '', patronymic: str = '') -> str:
        return ' '.join(self.get_list(surname, name, patronymic))

    def parse_list(self, full_name: list) -> tuple[str, str, str]:
        parts = {}
        for pos, item in enumerate(full_name):
            if pos >= len(self.__positions):
                break
            parts[self.__positions[pos]] = item if item else ""

        return str(parts.get('S', '')), str(parts.get('N', '')), str(parts.get('P', ''))

    def parse_str(self, full_name: str) -> tuple[str, str, str]:
        return self.parse_list(full_name.split())

    def __str__(self):
        return ''.join(self.__positions)


class Executor:

    def __init__(self, **params):
        self.variant = params.get('var', 0)

        if 'full_name' in params.keys():
            self.__pattern = Pattern(params.get("name_pattern"))
        else:
            self.__pattern = Pattern('SNP')

        self.surname, self.name, self.patronymic = self.__pattern.parse_str(params.get('full_name', "Ivanov Ivan Ivanovich"))

    def __str__(self):
        return self.__pattern.get_str(self.surname, self.name, self.patronymic)
