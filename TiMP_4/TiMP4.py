from word_parser import Document
from utils import bool_params_to_string


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

        params = {
            'img_1': "<w:p><w:r><w:t>%img_1%</w:t></w:r></w:p>",
            'img_2': "<w:p><w:r><w:t>%img_2%</w:t></w:r></w:p>",
            'img_3': "<w:p><w:r><w:t>%img_3%</w:t></w:r></w:p>"
        }

        self.__ptr_move('P')

        # Image
        self.__ptr('Q1', 'Q')
        # Image
        self.__ptr_move('Q')
        # Image

        self.document.add_step('A1', **params)
        self.A2()

    def A2(self):
        print("A2: Comparing ABC(P) and ABC(Q)")
        self.steps.append('A2')

        params = {
            # Images temp
            'img_1': "<w:p><w:r><w:t>%img_1%</w:t></w:r></w:p>",
            'img_2': "<w:p><w:r><w:t>%img_2%</w:t></w:r></w:p>",
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
        params['a_lt'] = params['a_p'] < params['a_q']
        params['a_eq'] = params['a_p'] == params['a_q']
        params['b_lt'] = params['b_p'] < params['b_q']
        params['b_eq'] = params['b_p'] == params['b_q']
        params['c_lt'] = params['c_p'] < params['c_q']
        params['c_eq'] = params['c_p'] == params['c_q']
        params['p_lt'] = params['psum'] < params['qsum']
        params['p_eq'] = params['psum'] == params['qsum']

        params['a_eq_and_b_lt'] = params['a_eq'] and params['b_lt']
        params['a_lt_and_b_lt'] = params['a_lt'] and params['b_lt']
        params['a_eq_and_b_eq'] = params['a_eq'] and params['b_eq']
        params['a_lt_or_a_eq_and_b_lt'] = params['a_lt'] or params['a_eq_and_b_lt']
        params['p_eq_and_a_lt_or_a_eq_and_b_lt'] = params['p_eq'] and params['a_lt_or_a_eq_and_b_lt']
        params['abc_p_lt'] = params['p_lt'] or params['p_eq_and_a_lt_or_a_eq_and_b_lt']
        params['abc_p_eq'] = params['a_eq_and_b_eq'] and params['c_eq']

        params_str = bool_params_to_string(params)
        self.document.add_step('A2')
        self.document.add_step('A2_cond_ltr', **params_str)

        if params['abc_p_lt']:
            self.__ptr('Q1', 'Q')
            # Image
            self.__ptr_move('Q')
            # Image

            self.document.add_step('A2_ltr', **params_str)
            self.A2()
        elif params['abc_p_eq']:
            self.document.add_step('A2_cond_eq', **params_str)
            self.A3()
        else:
            self.document.add_step('A2_gtr', **params_str)
            self.A5()

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
        print("A4: Excluding part")
        self.steps.append('A4')

        params = {
            'img_1': "<w:p><w:r><w:t>%img_1%</w:t></w:r></w:p>",
            'img_2': "<w:p><w:r><w:t>%img_2%</w:t></w:r></w:p>",
            'img_3': "<w:p><w:r><w:t>%img_3%</w:t></w:r></w:p>",
            'img_4': "<w:p><w:r><w:t>%img_4%</w:t></w:r></w:p>",
            'img_5': "<w:p><w:r><w:t>%img_5%</w:t></w:r></w:p>",
            'img_6': "<w:p><w:r><w:t>%img_6%</w:t></w:r></w:p>",
        }

        self.document.add_step('A4', **params)
        # self.A2()

    def A5(self):
        print("A5: Appending new part")
        self.steps.append('A5')

        params = {
            'img_1': "<w:p><w:r><w:t>%img_1%</w:t></w:r></w:p>",
            'img_2': "<w:p><w:r><w:t>%img_2%</w:t></w:r></w:p>",
            'img_3': "<w:p><w:r><w:t>%img_3%</w:t></w:r></w:p>",
            'img_4': "<w:p><w:r><w:t>%img_4%</w:t></w:r></w:p>",
            'img_5': "<w:p><w:r><w:t>%img_5%</w:t></w:r></w:p>",
            'img_6': "<w:p><w:r><w:t>%img_6%</w:t></w:r></w:p>",
        }

        self.document.add_step('A5', **params)
        # self.A2()
