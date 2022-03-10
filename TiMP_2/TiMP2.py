from math import floor

from TiMP_2.word_parser import Document


class Laba2:

    @staticmethod
    def parse_sequence(sequence: str) -> list:
        return [int(sequence[i]) - 1 for i in range(1, len(sequence), 2)]

    def get_args(self, res: dict = None) -> dict:
        if res is None:
            res = {}

        for i, b in enumerate(self.base):
            res[f"base_{i + 1}"] = str(b)
        for i, t in enumerate(self.top):
            res[f"top_{i + 1}"] = str(t)

        return res

    def __init__(self, task: dict, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/{filename}.doc")

        # Task
        self.base = task['BASE']
        self.top = task['TOP']
        self.oldtop = task['TOP'].copy()
        self.sequence = self.parse_sequence(task['SEQUENCE'])
        self.sequence_str = task['SEQUENCE']

        # Data
        self.var = var
        self.name = name

        self.i = -1
        self.j = -1

        # Repacking
        self.sum = 20
        self.inc = 0
        self.d = [0, 0, 0, 0]

        self.alpha = 0.0
        self.beta = 0.0
        self.sigma = 0
        self.tau = 0.0

        self.new_base = [-1, -1, -1, -1]

    def test(self):
        self.document.add_step("repacking/G2")
        self.document.add_step("repacking/G2_step")
        self.document.add_step("repacking/G2_true")
        self.document.add_step("repacking/G2_false")
        self.document.add_step("repacking/G2_end")

    def run(self):
        # return self.test()
        self.document.add_step("_title_page", var=self.var, name=self.name)
        self.document.add_step("_task", **self.get_args({"task": self.sequence_str}))

        self.document.add_step('practice')

        self.init()

        # Magic

        self.document.add_step("_conclusion")

    def init(self):
        self.document.add_step("init/memory", **self.get_args())
        self.memory_table()
        self.document.br()

        self.document.add_step("init/oldtop", **self.get_args())

        self.document.add_step("append/start", task=self.sequence_str)

        for stack in self.sequence:
            if self.append_step(stack):
                self.repack()
                self.move()

    def memory_table(self):
        content = {}
        for i in range(4):
            for stack_i, cell_i in enumerate(range(self.base[i] + 1, self.top[i] + 1)):
                content[cell_i] = (i + 1, stack_i + 1)

        cells = []
        for i in range(20):
            if content.get(i):
                cells.append(self.document.get_step_xml("memory_table/cell", stack=content[i][0], cell=content[i][1]))
            else:
                cells.append(self.document.get_step_xml("memory_table/cell_empty"))

        self.document.add_step("memory_table/base", cells="".join(cells))

    def append_step(self, stack: int):
        nums = [
            "в первый",
            "во второй",
            "в третий",
            "в четвертый"
        ]

        self.top[stack] += 1
        params = {
            'i': stack + 1,
            'i_str': nums[stack],
            'i_inc': stack + 2,
            'top_i': self.top[stack],
            'top_i_dec': self.top[stack] - 1,
            'base_i_inc': self.base[stack + 1]
        }

        self.document.add_step("append/step", **params)

        overflow = self.top[stack] > self.base[stack + 1]
        if overflow:
            self.document.add_step("append/step_true", **params)
            self.i = stack
        else:
            self.document.add_step("append/step_false", **params)

        self.memory_table()

        self.document.add_step("append/end", **self.get_args())

        return overflow

    # ===== Repacking ===== #
    def repack(self):
        self.document.add_step("repacking/_start")

        self.G1()
        self.G2()
        if self.G3():  # Memory full
            return
        self.G4()
        self.G5()
        self.G6()

        self.document.add_step("repacking/_stop")

    def G1(self):
        self.sum = 20
        self.inc = 0

        self.document.add_step("repacking/G1")

    def G2(self):
        self.document.add_step("repacking/G2")

        for j in range(4):
            params = {
                'sum_old': self.sum,
                'j': j + 1,
                'top_j': self.top[j],
                'base_j': self.base[j] if self.base[j] >= 0 else f"({self.base[j]})",
                'top_subtract_base': self.top[j] - self.base[j],
                'oldtop_j': self.oldtop[j],
                'inc_old': self.inc
            }
            self.sum -= params['top_subtract_base']
            params['sum'] = self.sum

            self.document.add_step("repacking/G2_step", **params)

            if self.top[j] > self.oldtop[j]:
                self.d[j] = self.top[j] - self.oldtop[j]
                params['d_j'] = self.d[j]
                self.inc += self.d[j]
                params['inc'] = self.inc
                self.document.add_step("repacking/G2_true", **params)
            else:
                self.d[j] = 0
                self.document.add_step("repacking/G2_false", **params)

        self.document.add_step("repacking/G2_end", sum=self.sum, inc=self.inc)

    def G3(self):
        condition = self.sum < 0
        self.document.add_step("repacking/G3_" + ("true" if condition else "false"), sum=self.sum)
        return condition

    def G4(self):
        self.alpha = 0.1 * self.sum / 4
        self.beta = 0.9 * self.sum / self.inc
        self.document.add_step("repacking/G4", sum=self.sum, inc=self.inc, alpha=self.alpha, beta=self.beta)

    def G5(self):
        self.new_base[0] = self.base[0]
        self.sigma = 0
        self.document.add_step("repacking/G5", newbase_1=self.base[0])

        for j in range(1, 4):
            self.tau = self.sigma + self.alpha + self.d[j - 1] * self.beta
            self.new_base[j] = self.new_base[j - 1] + self.top[j - 1] - self.base[j - 1] + floor(self.tau) - floor(
                self.sigma)
            params = {
                'j': j + 1,
                'j_dec': j,
                'alpha': self.alpha,
                'beta': self.beta,
                'sigma': 0,
                'tau': self.tau,
                'd_j_dec': self.d[j - 1],
                'sigma_plus_alpha': self.sigma + self.alpha,
                'newbase_j': self.new_base[j],
                'newbase_j_dec': self.new_base[j - 1],
                'top_j_dec': self.top[j - 1],
                'base_j_dec': self.base[j - 1] if self.base[j - 1] >= 0 else f"({self.base[j - 1]})",
                'tau_int': floor(self.tau),
                'sigma_int': floor(self.sigma)
            }
            self.sigma = self.tau

            self.document.add_step("repacking/G5_step", **params)

    def G6(self):
        params = {
            'i': self.i + 1,
            'top_i_inc': self.top[self.i]
        }
        self.top[self.i] -= 1
        params['top_i'] = self.top[self.i]

        self.document.add_step("repacking/G6", **params)

        self.memory_table()
        self.document.add_step("append/end", **self.get_args())

    # ===================== #

    # ====== Moving ======= #
    def move(self):
        self.document.add_step("moving/_start")

        self.R1()
        self.R2()

    def R1(self):
        self.j = 1
        self.document.add_step('moving/R1')

    def R2(self):
        goto_r3 = "ИСТИНА, следовательно, перейти к шагу R3"
        goto_r4 = "ИСТИНА, следовательно, перейти к шагу R4"
        next_cond = "ЛОЖЬ, проверяем следующее условие"
        repeat_r2 = "ЛОЖЬ, следовательно, выполняем шаг R2 сначала"
        end_r = "ИСТИНА, следовательно, окончить алгоритм R"

        params = {
            'j': self.j + 1,
            'j_dec': self.j,
            'newbase_j': self.new_base[self.j],
            'base_j': self.base[self.j],
            'cond_1': self.new_base[self.j] < self.base[self.j],
            'cond_2': self.new_base[self.j] > self.base[self.j],
            'cond_3': self.j > 4,
        }

        self.document.add_step("moving/R2", **params)
        self.j += 1

        params['result'] = goto_r3 if params['cond_1'] else next_cond
        self.document.add_step('moving/R2_cond1', **params)
        if params['cond_1']:
            self.R3()
            return

        params['result'] = goto_r4 if params['cond_2'] else next_cond
        self.document.add_step('moving/R2_cond2', **params)
        if params['cond_2']:
            self.R4()
            return

        params['result'] = end_r if params['cond_3'] else repeat_r2
        self.document.add_step('moving/R2_cond3', **params)
        if not params['cond_3']:
            self.R2()

    def R3(self):
        pass

    def R4(self):
        pass

    def R5(self):
        pass

    def R6(self):
        pass
    # ===================== #
