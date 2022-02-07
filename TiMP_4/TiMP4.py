from word_parser import Document


class Laba4:
    def __init__(self, polynomial_1: list, polynomial_2: list, name="out"):
        # Document
        self.document = Document(f"output/docs/{name}.doc")

        # Data
        self.pols = [
            polynomial_1,
            polynomial_2
        ]

        # Pointers
        self.pointers = {'P': [0, len(self.pols[0]) - 1], 'Q': [1, len(self.pols[1]) - 1]}

        # Answer
        self.steps = []

    def __ptr(self, name: str, val=None):
        if val:
            if name not in self.pointers.keys():
                self.pointers[name] = (0, 0)
            if type(val) is int:
                self.pointers[name][1] = val
            elif type(val) is list or type(val) is tuple:
                self.pointers[name] = val
            elif type(val) is str:
                self.pointers[name] = self.pointers[val]
        else:
            ptr = self.pointers.get(name)
            return self.pols[ptr[0]][ptr[1]]

    def __ptr_move(self, name: str):
        self.pointers[name][1] += 1
        ptr = self.pointers[name]
        if ptr[1] >= len(self.pols[ptr[0]]):
            self.pointers[name][1] = 0

    def run(self):
        self.A1()

    def A1(self):
        print("A1: Initialization")
        self.steps.append('A1')

        self.__ptr_move('P')
        # Image
        self.__ptr('Q1', 'Q')
        # Image
        self.__ptr_move('Q')
        # Image

        self.document.add_step('A1')
        self.A2()

    def A2(self):
        print("A2: Comparing ABC(P) and ABC(Q)")
        self.steps.append('A2')

        params = {
            # P
            'a_p': self.__ptr('P')[1],
            'b_p': self.__ptr('P')[2],
            'c_p': self.__ptr('P')[3],
            # Q
            'a_q': self.__ptr('Q')[1],
            'b_q': self.__ptr('Q')[2],
            'c_q': self.__ptr('Q')[3],
            # Sum
            'psum': sum(self.__ptr('P')[1:]),
            'qsum': sum(self.__ptr('Q')[1:]),
        }

        # Conditions
        params['a_lt'] = "ИСТИНА" if params['a_p'] < params['a_q'] else "ЛОЖЬ"
        params['a_eq'] = "ИСТИНА" if params['a_p'] == params['a_q'] else "ЛОЖЬ"
        params['b_lt'] = "ИСТИНА" if params['b_p'] < params['b_q'] else "ЛОЖЬ"
        params['p_lt'] = "ИСТИНА" if params['psum'] < params['qsum'] else "ЛОЖЬ"
        params['p_eq'] = "ИСТИНА" if params['psum'] == params['qsum'] else "ЛОЖЬ"

        params['a_eq_and_b_lt'] = params['a_eq'] and params['b_lt']
        params['a_lt_or_a_eq_and_b_lt'] = params['a_lt'] or params['a_eq_and_b_lt']
        params['p_eq_and_a_lt_or_a_eq_and_b_lt'] = params['p_eq'] and params['a_lt_or_a_eq_and_b_lt']
        params['res'] = params['p_lt'] or params['p_eq_and_a_lt_or_a_eq_and_b_lt']

        self.document.add_step('A2_cond', **params)

        if params['res'] == "ИСТИНА":
            self.__ptr('Q1', 'Q')
            # Image
            self.__ptr_move('Q')
            # Image

            self.document.add_step('A2_true')
            self.A2()
        else:
            # Conditions
            params['c_lt'] = "ИСТИНА" if params['c_p'] < params['c_q'] else "ЛОЖЬ"
            params['a_lt_and_b_lt'] = "ИСТИНА" if params['a_lt'] and params['b_lt'] else "ЛОЖЬ"
            params['res'] = "ИСТИНА" if params['a_lt_and_b_lt'] and params['c_lt'] else "ЛОЖЬ"

            self.document.add_step('A2_false_cond', **params)
            if params['res'] == "ИСТИНА":
                self.document.add_step('A2_false_true')
                self.A3()
            else:
                self.document.add_step('A2_false_false_cond')

    def A3(self):
        print("A3: Summation")
        self.steps.append('A3')

        params = {}

        if self.__ptr('P')[1:] < (0, 0, 0):
            pass
        else:
            params['coef_q_prev'] = self.__ptr('Q')[0]
            params['coef_p'] = self.__ptr('P')[0]

            #self.__ptr('Q')[0] = self.__ptr('P')[0]
            #params['coef_q'] = self.__ptr('Q')[0]

    def A4(self):
        print("A4: ")
        self.steps.append('A4')

        pass

    def A5(self):
        print("A5: ")
        self.steps.append('A5')

        pass
