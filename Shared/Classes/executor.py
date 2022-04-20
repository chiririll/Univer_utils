class Pattern:
    """ Pattern for parsing and formatting full name """

    def __init__(self, pattern: str = None):
        if pattern is None:
            pattern = 'SNP'

        self.__positions = []
        self.update_pattern(pattern)

    def update_pattern(self, pattern: str) -> None:
        """
        Method for applying new pattern
        @param pattern: pattern string (S - surname, N - name, P - patronymic)
        """
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
        """
        Method for ordering full name
        @return: List with ordered full name
        """
        items = {'S': surname, 'N': name, 'P': patronymic}
        return list(map(lambda pos: items[pos], self.__positions))

    def get_str(self, surname: str = '', name: str = '', patronymic: str = '') -> str:
        """
        Method for ordering full name
        @return: String with ordered full name
        """
        return ' '.join(self.get_list(surname, name, patronymic))

    def parse_list(self, *full_name: str) -> tuple[str, str, str]:
        """
        Method for parsing list with surname name and patronymic according to pattern
        @param full_name: surname name and patronymic ordered by pattern
        @return: tuple (surname, name, patronymic)
        """
        parts = {}
        for pos, item in enumerate(full_name):
            if pos >= len(self.__positions):
                break
            parts[self.__positions[pos]] = item if item else ""

        return str(parts.get('S', '')), str(parts.get('N', '')), str(parts.get('P', ''))

    def parse_str(self, full_name: str) -> tuple[str, str, str]:
        """
        Method for parsing string with surname name and patronymic according to pattern
        @param full_name: sting with full_name, ordered by pattern
        @return: tuple (surname, name, patronymic)
        """
        return self.parse_list(*full_name.split())

    def __str__(self):
        return ''.join(self.__positions)


class Executor:
    """ Class for representing student (full name and variant) """
    def __init__(self, name: str = "Ivanov Ivan Ivanovich", var: int = 0, pattern: Pattern | str = 'SNP', **params):
        self.variant = var

        if type(pattern) is str:
            self.__pattern = Pattern(pattern)
        else:
            self.__pattern = pattern

        self.surname, self.name, self.patronymic = self.__pattern.parse_str(name)

    def __str__(self):
        return self.__pattern.get_str(self.surname, self.name, self.patronymic)
