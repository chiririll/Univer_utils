from word_parser import Document
from drawer import draw


DEFAULT_IMG = "<w:p><w:r><w:t>%image%</w:t></w:r></w:p>"


class Laba4:
    def __init__(self, task: list, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/docs/{filename}.doc")

        # Data
        self.task = task
        self.var = var
        self.name = name

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
                self.pointers[name] = [0, 0]
            # Change position inside polynomial
            if type(val) is int:
                self.pointers[name][1] = val
            # Change position and polynomial
            elif type(val) is list:
                self.pointers[name] = val.copy()
            elif type(val) is tuple:
                self.pointers[name] = list(val)
            # Move one pointer to another
            elif type(val) is str:
                self.pointers[name] = self.pointers[val].copy()
        else:
            # Returning pointer
            ptr = self.pointers.get(name)
            return self.pols[ptr[0]][ptr[1]]

    def __ptr_move(self, name: str):
        ptr = self.pointers[name]
        # Moving to next link
        self.pointers[name][1] = self.pols[ptr[0]][ptr[1]][4]

    def __add_part(self, pol: int = 0, pos: int = 0, ptr: str = None):
        if ptr:
            pol, pos = self.pointers[ptr]

        # Updating links
        for i in range(pos - 1, len(self.pols[pol]) - 1):
            self.pols[pol][i][4] = (self.pols[pol][i][4] + 1) % (len(self.pols[pol]) + 1)

        # Moving pointers
        for k, v in self.pointers.items():
            if k != ptr and v[0] == pol and v[1] >= pos:
                self.pointers[k][1] += 1

        # Adding part
        self.pols[pol].insert(pos, [None, None, None, None, None])

    def __exclude_part(self, pol: int = 0, pos: int = 0, ptr: str = None):
        if ptr:
            pol, pos = self.pointers[ptr]

        # Updating links
        for i in range(pos + 1, len(self.pols[pol]) - 1):
            self.pols[pol][i][4] -= 1

        # Moving pointers
        self.pointers.pop(ptr)
        for k, v in self.pointers.items():
            if v[0] == pol and v[1] >= pos:
                self.pointers[k][1] -= 1

        # Excluding part
        self.pols[pol].pop(pos)

    def run(self):
        self.document.add_step('_title_page', var=self.var, name=self.name)

        img_1 = draw('A0/A0', self.pols, self.pointers)

        self.document.add_step('_practice', img_1=img_1)

        self.A1()

    def finish(self):
        def generate_pol(pol: list):
            res = []
            for i, part in enumerate(pol):
                if part[0] == 0:
                    continue
                valid = abs(part[0]) != 1

                if i > 0:
                    res.append((" - " if part[0] < 0 else " + ") + (str(abs(part[0])) if abs(part[0]) != 1 else ""))
                elif abs(part[0]) != 1:
                    res.append(str(part[0]))
                elif part[0] < 0:
                    res.append('-')

                variables = ['x', 'y', 'z']
                for i in range(1, 4):
                    if part[i] != 0:
                        valid = True
                        res.append(variables[i - 1])
                        res.append('^' + (str(part[i]) if part[i] != 1 else ""))

                if not valid:
                    res.append("1")
            return res

        def generate_xml(equation: list):
            res = "<w:r><w:t xml:space=\"preserve\">"
            for p in equation:
                if p[0] == '^':
                    res += "</w:t></w:r>"
                    res += "<w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t xml:space=\"preserve\">"
                    res += p[1:]
                    res += "</w:t></w:r><w:r><w:t xml:space=\"preserve\">"
                else:
                    res += p
            res += "</w:t></w:r>"
            return res

        params = {
            'steps': ", ".join(self.steps),
            'polynomial_1': generate_xml(generate_pol(self.task[0])),
            'polynomial_2': generate_xml(generate_pol(self.task[1])),
            'polynomial_answer': generate_xml(generate_pol(self.pols[1])),
        }

        self.document.add_step('_answer', **params)
        self.document.add_step('_conclusion')

    def A1(self):
        print("A1: Initialization")
        self.steps.append('A1')

        params = {}

        self.__ptr_move('P')
        params['img_1'] = draw('A1/img_1', self.pols, self.pointers)

        self.__ptr('Q1', 'Q')
        params['img_2'] = draw('A1/img_2', self.pols, self.pointers)

        self.__ptr_move('Q')
        params['img_3'] = draw('A1/img_3', self.pols, self.pointers)

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
            'psum': sum(self.__ptr('P')[1:-1]),
            'qsum': sum(self.__ptr('Q')[1:-1]),
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
            params['img_1'] = draw('A2/img_1', self.pols, self.pointers)

            self.__ptr_move('Q')
            params['img_2'] = draw('A2/img_2', self.pols, self.pointers)

            self.document.add_step('A2_ltr', **params)
            self.A2()
            return

        self.document.add_step('A2_cond_eq', **params)
        if params['abc_p_eq']:    # ABC(P) = ABC(Q)
            self.document.add_step('A2_eq', **params)
            self.A3()
            return

        # ABC(P) > ABC(Q)
        self.document.add_step('A2_gtr', **params)
        self.A5()

    def A3(self):
        def abc_str(ptr: str):
            abc = ""
            for s in self.__ptr(ptr)[1:-1]:
                abc += str(s)
            return abc

        print("A3: Summation")
        self.steps.append('A3')

        params = {
            'abc_p': abc_str('P'),
            'abc_p_ltr_0': self.__ptr('P')[1:-1] < [0, 0, 0],
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
            params['img_1'] = draw('A3/img_1', self.pols, self.pointers)

            self.document.add_step('A3_cond_zero', **params)

            if params['coef_q_eq_0']:
                self.document.add_step('A3_zero', **params)
                self.A4()
            else:
                self.__ptr('Q1', 'Q')
                params['img_2'] = draw('A3/img_2', self.pols, self.pointers)

                self.__ptr_move('P')
                params['img_3'] = draw('A3/img_3', self.pols, self.pointers)

                self.__ptr_move('Q')
                params['img_4'] = draw('A3/img_4', self.pols, self.pointers)

                self.document.add_step('A3_non_zero', **params)
                self.A2()

    def A4(self):
        print("A4: Excluding part")
        self.steps.append('A4')

        params = {}

        self.__ptr('Q2', 'Q')
        params['img_1'] = draw('A4/img_1', self.pols, self.pointers)

        self.__ptr_move('Q')
        params['img_2'] = draw('A4/img_2', self.pols, self.pointers)

        # LINK(Q1) = Q
        self.__ptr('Q1')[4] = self.pointers['Q'][1]
        params['img_3'] = DEFAULT_IMG
        params['img_3'] = draw('A4/img_3', self.pols, self.pointers)

        # AVAIL <- Q2
        self.__exclude_part(ptr='Q2')
        self.__ptr('Q1')[4] = self.pointers['Q'][1]
        params['img_4'] = draw('A4/img_4', self.pols, self.pointers)

        # P <- LINK(P)
        self.__ptr_move('P')
        params['img_5'] = draw('A4/img_5', self.pols, self.pointers)

        self.document.add_step('A4', **params)
        self.A2()

    def A5(self):
        print("A5: Appending new part")
        self.steps.append('A5')

        params = {}

        # Q2 <- AVAIL
        self.__ptr('Q2', (1, (self.__ptr('Q')[4] - 1) % len(self.pols[1])))
        self.__add_part(ptr='Q2')
        params['img_1'] = draw('A5/img_1', self.pols, self.pointers)

        # COEF(Q2) <- COEF(P)
        self.__ptr('Q2')[0] = self.__ptr('P')[0]
        params['img_2'] = draw('A5/img_2', self.pols, self.pointers)

        # ABC(Q2) <- ABC(P)
        self.__ptr('Q2')[1] = self.__ptr('P')[1]
        self.__ptr('Q2')[2] = self.__ptr('P')[2]
        self.__ptr('Q2')[3] = self.__ptr('P')[3]
        params['img_3'] = draw('A5/img_3', self.pols, self.pointers)

        # LINK(Q2) <- Q
        self.__ptr('Q2')[4] = self.pointers['Q'][1]
        params['img_4'] = draw('A5/img_4', self.pols, self.pointers)

        # LINK(Q1) <- Q2
        self.__ptr('Q1')[4] = self.pointers['Q2'][1]
        params['img_5'] = draw('A5/img_5', self.pols, self.pointers)

        # Q1 <- Q2
        self.__ptr('Q1', 'Q2')
        params['img_6'] = draw('A5/img_6', self.pols, self.pointers)

        # P <- LINK(P)
        self.__ptr_move('P')
        params['img_7'] = draw('A5/img_7', self.pols, self.pointers)

        self.document.add_step('A5', **params)
        self.A2()
