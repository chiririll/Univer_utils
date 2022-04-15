import random

import Shared

from . import drawer


class Laba1(Shared.Classes.Laba):

    laba = {
        'number': "1",
        'title': "ЛИНЕЙНЫЕ ИНФОРМАЦИОННЫЕ СТРУКТУРЫ",
        'subject': "TiMP",
        'name': "laba1"
    }

    def __init__(self, task: list, **params):
        # Task  [TOP, ..., BOTTOM]
        # Cards [BOTTOM, ..., TOP]
        # Card  [TAG, SUIT, RANK]
        self.cards = self.prepare_task(task)

        params['word_params'] = {
            'parts_folder': "TiMP/TiMP_1/steps"
        }

        # Data
        super().__init__(**params)

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
        self.document.add_step('title_pages/TiMP')
        self.task()

        # self.program()
        # self.result()
        # self.protocol()

        # self.document.add_step('_conclusion')

    def task(self):
        positions = ["первая", "вторая", "третья", "четвертая", "пятая", "шестая", "седьмая", "восьмая", "девятая"]
        cards = []
        for i, c in enumerate(reversed(self.cards)):
            card = "- "
            card += "верхняя карта" if i == 0 else f"{positions[i]} сверху"
            card += " (нижняя)" if i >= len(self.cards) - 1 else ""
            card += f": " + self.card_to_string(c, 'ADDR') + ", "

            cards.append(f"<w:p><w:r><w:t>{card}</w:t></w:r></w:p>")
        self.document.add_step('_task', cards=cards)

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
                'image_1': drawer.draw_cards(self.cards[:i+1]),
                'image_2': drawer.draw_scheme(f"prog_{i}", self.cards[:i+1])
            }
            for j in range(i + 1):
                next_card = "Λ" if j <= 0 else self.cards[j - 1]['ADDR']
                params['cards'] += self.document.get_step_xml('PROTOCOL/card', **self.cards[j], NEXT=next_card)

            self.document.add_step('PROTOCOL/step', **params)

        print("Counting cards")
        self.document.add_step('PROTOCOL/counting/start')

        self.document.add_step('PROTOCOL/counting/B1', **self.cards[-1], image=drawer.draw_scheme(f"count_{0}", self.cards, 0))
        for i in range(1, len(self.cards) + 1):
            img = drawer.draw_scheme(f"count_{i}", self.cards, min(i, len(self.cards) - 1), i < len(self.cards))
            addr = "NULL" if i >= len(self.cards) else self.cards[-i-1]['ADDR']
            self.document.add_step('PROTOCOL/counting/B2', **self.cards[-i], is_null=False)
            self.document.add_step('PROTOCOL/counting/B3', n=i-1, n_1=i, ADDR=addr, image=img)

        self.document.add_step('PROTOCOL/counting/B2', ADDR="NULL", is_null=True)
        self.document.add_step('PROTOCOL/counting/end', n=len(self.cards))
