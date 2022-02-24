import random

from word_parser import Document
from drawer import draw_cards, draw_scheme


class Laba1:

    def __init__(self, task: list, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/{filename}.doc")

        # Task  [TOP, ..., BOTTOM]
        # Cards [BOTTOM, ..., TOP]
        # Card  [TAG, SUIT, RANK]
        self.cards = self.prepare_task(task)

        # Data
        self.var = var
        self.name = name

    @staticmethod
    def prepare_task(task) -> list:
        card_size = 32
        base = random.randint(2 ** 8, 2 ** 16 - len(task) * card_size - 1)

        cards = []
        for i, card in enumerate(reversed(task)):
            cards.append(
                {'TAG': card[0], 'SUIT': card[1], 'RANK': card[2], 'ADDR': f'{base + i * card_size:0>4X}'}
            )

        return cards

    @staticmethod
    def card_to_string(card: dict, *exclude: str) -> str:
        string = ""
        for k, v in card.items():
            if k not in exclude:
                string += f"{k} = {v}, "
        return string[:-2]

    def run(self):
        self.document.add_step('_title_page', var=self.var, name=self.name)
        self.task()

        self.program()
        self.result()
        self.protocol()

    def task(self):
        positions = ["первая", "вторая", "третья", "четвертая", "пятая", "шестая", "седьмая", "восьмая", "девятая"]
        cards_xml = []
        for i, c in enumerate(reversed(self.cards)):
            card = "- "
            card += "верхняя карта" if i == 0 else f"{positions[i]} сверху"
            card += " (нижняя)" if i >= len(self.cards) - 1 else ""
            card += f": " + self.card_to_string(c, 'ADDR') + ", "

            cards_xml.append(f"<w:p><w:r><w:t>{card}</w:t></w:r></w:p>")
        self.document.add_step('_task', cards="\n".join(cards_xml))

    def program(self):
        print("Generating program")

        self.document.add_step('PROG/start')

        for i in range(len(self.cards)):
            self.program_card(i)

        self.document.add_step('PROG/end')

    def program_card(self, i: int):
        def get_comment(index: int) -> str:
            if index >= len(self.cards) - 1:
                return "Добавление верхней карты в стопку"
            if index == 0:
                return "Помещение нижней карты в пустую стопку"
            else:
                return "Добавление новой карты в стопку сверху"

        print(f"\t Adding program card #{i}: {self.card_to_string(self.cards[i])}")
        self.document.add_step('PROG/card', comment=get_comment(i), **self.cards[i])

    def result(self):
        print("Generating result")

        self.document.add_step('RESULT/start')

        for i, c in enumerate(self.cards):
            self.document.add_step('RESULT/card', card_addr=c['ADDR'])

        params = {
            'top_tag': self.cards[-1]['TAG'],
            'top_suit': self.cards[-1]['SUIT'],
            'top_next_rank': self.cards[-2]['RANK'],
            'n': len(self.cards),
        }
        self.document.add_step('RESULT/end', **params)

    def protocol(self):
        print("Generating protocol")

        self.document.add_step('PROTOCOL/protocol')

        for i, top in enumerate(self.cards):
            self.program_card(i)

            params = {
                'cards': "",
                'top_addr': top['ADDR'],
                'image_1': draw_cards(self.cards[:i+1]),
                'image_2': draw_scheme(f"prog_{i}", self.cards[:i+1])
            }
            for j in range(i + 1):
                next_card = "Λ" if j <= 0 else self.cards[j - 1]['ADDR']
                params['cards'] += self.document.get_step_xml('PROTOCOL/card', **self.cards[j], NEXT=next_card)

            self.document.add_step('PROTOCOL/step', **params)
