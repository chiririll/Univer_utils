from word_parser import Document


DEFAULT_IMG = "<w:p><w:r><w:t>%image%</w:t></w:r></w:p>"


class Laba4:
    def __init__(self, task: list, name="out"):
        # Document
        self.document = Document(f"output/docs/{name}.doc")

        self.task = []

        # Data
        self.task = task
        # Part: [COEF, A, B, C, NEXT_INDEX]
        self.pols = []
        self.__parse_task()

        # Pointers
        self.pointers = {'P': [0, len(self.pols[0]) - 1], 'Q': [1, len(self.pols[1]) - 1]}

        # Answer
        self.steps = []

    def __parse_task(self):
        # [COEF, A, B, C]
        for pol in self.task:
            new_pol = []
            for i, part in enumerate(pol):
                new_part = list(part)
                new_part.append((i+1) % len(pol))
                new_pol.append(new_part)
            self.pols.append(new_pol)

    def __ptr(self, name: str, val=None):
        # Editing pointer
        if val:
            # Create new pointer and set default position
            if name not in self.pointers.keys():
                self.pointers[name] = (0, 0)
            # Change position inside polynomial
            if type(val) is int:
                self.pointers[name][1] = val
            # Change position and polynomial
            elif type(val) is list or type(val) is tuple:
                self.pointers[name] = val
            # Move one pointer to another
            elif type(val) is str:
                self.pointers[name] = self.pointers[val]
        else:
            # Returning pointer
            ptr = self.pointers.get(name)
            return self.pols[ptr[0]][ptr[1]]

    def __ptr_move(self, name: str):
        ptr = self.pointers[name]
        # Moving to next link
        self.pointers[name][1] = self.pols[ptr[0]][ptr[1]][4]

    def run(self):
        # self.document.add_step('_title_page')

        img_1 = DEFAULT_IMG
        self.document.add_step('_practice', img_1=img_1)

        self.A1()

    def finish(self):
        self.document.add_step('_answer', steps=', '.join(self.steps))
        self.document.add_step('conclusion')

    def A1(self):
        print("A1: Initialization")
        self.steps.append('A1')

        params = {
            'img_1': DEFAULT_IMG,
            'img_2': DEFAULT_IMG,
            'img_3': DEFAULT_IMG
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

        self.document.add_step('A2')
        self.document.add_step('A2_cond_ltr', **params)

        if params['abc_p_lt']:      # ABC(P) < ABC(Q)
            self.__ptr('Q1', 'Q')
            params['img_1'] = DEFAULT_IMG
            self.__ptr_move('Q')
            params['img_2'] = DEFAULT_IMG

            self.document.add_step('A2_ltr', **params)
            self.A2()
        elif params['abc_p_eq']:    # ABC(P) = ABC(Q)
            self.document.add_step('A2_cond_eq', **params)
            self.A3()
        else:                       # ABC(P) > ABC(Q)
            self.document.add_step('A2_gtr', **params)
            self.A5()

    def A3(self):
        print("A3: Summation")
        self.steps.append('A3')

        params = {
            'abc_p': ''.join(self.__ptr('P')[1:]),
            'abc_p_ltr_0': self.__ptr('P')[1:] < (0, 0, 0),
            'coef_p': self.__ptr('P')[0],
            'coef_q': self.__ptr('Q')[0],
        }

        self.document.add_step('A3', **params)
        self.document.add_step('A3_cond_finish', **params)

        if params['abc_p_ltr_0']:
            self.document.add_step('A3_finish', **params)
            self.finish()
        else:
            self.__ptr('Q')[0] = self.__ptr('P')[0] + self.__ptr('Q')[0]
            params['coef_q_new'] = self.__ptr('Q')[0]
            params['coef_q_eq_0'] = self.__ptr('Q')[0] == 0

            params['img_1'] = DEFAULT_IMG

            self.document.add_step('A3_cond_zero', **params)

            if params['coef_q_eq_0']:
                self.document.add_step('A3_zero', **params)
                self.A4()
            else:
                self.__ptr('Q1', 'Q')
                params['img_2'] = DEFAULT_IMG

                self.__ptr_move('P')
                params['img_3'] = DEFAULT_IMG

                self.__ptr_move('Q')
                params['img_4'] = DEFAULT_IMG

                self.document.add_step('A3_non_zero', **params)
                self.A2()

    def A4(self):
        print("A4: Excluding part")
        self.steps.append('A4')

        params = {}

        self.__ptr('Q2', 'Q')
        params['img_1'] = DEFAULT_IMG

        self.__ptr_move('Q')
        params['img_2'] = DEFAULT_IMG

        # TODO: LINK(Q1) = Q
        params['img_3'] = DEFAULT_IMG

        # TODO: AVAIL <- Q2
        params['img_4'] = DEFAULT_IMG

        self.document.add_step('A4', **params)
        # self.A2()

    def A5(self):
        print("A5: Appending new part")
        self.steps.append('A5')

        params = {
            'img_1': DEFAULT_IMG,
            'img_2': DEFAULT_IMG,
            'img_3': DEFAULT_IMG,
            'img_4': DEFAULT_IMG,
            'img_5': DEFAULT_IMG,
            'img_6': DEFAULT_IMG,
        }

        # Q2 <- AAVAIL

        self.document.add_step('A5', **params)
        # self.A2()
