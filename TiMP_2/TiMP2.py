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
        self.base = task['BASE'] + [19]
        self.top = task['TOP']
        self.oldtop = task['TOP'].copy()
        self.sequence = self.parse_sequence(task['SEQUENCE'])
        self.sequence_str = task['SEQUENCE']
        self.memory = [0] * 20

        # Data
        self.var = var
        self.name = name

        self.i = -1
        self.j = -1
        self.k = -1

        # Repacking
        self.sum = 20
        self.inc = 0
        self.d = [0, 0, 0, 0]

        self.alpha = 0.0
        self.beta = 0.0
        self.delta = 0
        self.sigma = 0
        self.tau = 0.0

        self.new_base = self.base.copy()

    def run(self):
        self.document.add_step("_title_page", var=self.var, name=self.name)
        self.document.add_step("_task", **self.get_args({"task": self.sequence_str}))

        self.document.add_step('practice')

        self.init()

        self.document.add_step('_answer')
        self.memory_table(refresh_memory=False)

        self.document.add_step("_conclusion")

    def init(self):
        self.document.add_step("init/memory", **self.get_args())
        self.memory_table(False)
        self.document.br()

        self.document.add_step("init/oldtop", **self.get_args())

        self.document.add_step("append/start", task=self.sequence_str)

        for stack in self.sequence:
            if self.append_step(stack):
                self.repack()
                self.move()

    def memory_table(self, add_address: bool = True, refresh_memory: bool = True):
        def update_memory():
            content = {}
            for i in range(4):
                for stack_i, cell_i in enumerate(range(self.base[i] + 1, self.top[i] + 1)):
                    content[cell_i] = (i + 1, stack_i + 1)
            for i in range(20):
                self.memory[i] = content.get(i, 0)

        if refresh_memory:
            update_memory()

        cells = []
        for c in self.memory:
            if c:
                cells.append(self.document.get_step_xml("memory_table/cell", stack=c[0], cell=c[1]))
            else:
                cells.append(self.document.get_step_xml("memory_table/cell_empty"))

        self.document.add_step("memory_table/base", cells="".join(cells))
        if add_address:
            self.document.add_step("memory_table/end", **self.get_args())

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
        self.document.br()

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

    # ===================== #

    # ====== Moving ======= #
    def move(self):
        self.document.add_step("moving/_start")

        self.R1()
        while not self.R2():
            pass
        self.RG6()

    def R1(self):
        self.j = 0
        self.document.add_step('moving/R1')

    def R2(self):
        goto_r3 = "ИСТИНА, следовательно, перейти к шагу R3"
        goto_r4 = "ИСТИНА, следовательно, перейти к шагу R4"
        next_cond = "ЛОЖЬ, проверяем следующее условие"
        repeat_r2 = "ЛОЖЬ, следовательно, выполняем шаг R2 сначала"
        end_r = "ИСТИНА, следовательно, окончить алгоритм R"

        self.j += 1

        params = {
            'j': self.j + 1,
            'j_dec': self.j,
            'newbase_j': self.new_base[self.j],
            'base_j': self.base[self.j],
            'cond_1': self.new_base[self.j] < self.base[self.j],
            'cond_2': self.new_base[self.j] > self.base[self.j],
            'cond_3': self.j > 3,
        }

        self.document.add_step("moving/R2", **params)

        params['result'] = goto_r3 if params['cond_1'] else next_cond
        self.document.add_step('moving/R2_cond1', **params)
        if params['cond_1']:
            return self.R3()

        params['result'] = goto_r4 if params['cond_2'] else next_cond
        self.document.add_step('moving/R2_cond2', **params)
        if params['cond_2']:
            return self.R4()

        params['result'] = end_r if params['cond_3'] else repeat_r2
        self.document.add_step('moving/R2_cond3', **params)
        return params['cond_3']

    def R3(self):
        self.delta = self.base[self.j] - self.new_base[self.j]
        params = {
            'j': self.j + 1,
            'delta': self.delta,
            'base_j': self.base[self.j],
            'newbase_j': self.new_base[self.j],
            'top_j': self.top[self.j],
            'base_j_inc': self.base[self.j] + 1,
            'base_j_add2': self.base[self.j] + 2,
            'l': ', '.join(list(map(str, range(self.base[self.j] + 1, self.top[self.j] + 1))))
        }
        self.document.add_step('moving/R3', **params)

        for l in range(self.base[self.j], self.top[self.j]):
            params['l'] = l + 1
            params['l_subtract_delta'] = l - self.delta + 1

            self.document.add_step('moving/R3_step', **params)
            self.memory[l - self.delta + 1] = self.memory[l + 1]
            self.memory[l + 1] = 0
            self.memory_table(refresh_memory=False)

        self.base[self.j] = self.new_base[self.j]
        self.top[self.j] -= self.delta

        params['top_j_new'] = self.top[self.j]
        self.document.add_step('moving/R3_end', **params)
        self.memory_table()

    def R4(self):
        self.k = self.j
        self.document.add_step('moving/R4', j=self.j + 1)

        for self.k in range(self.j, 5):
            params = {
                'j': self.j + 1,
                'k': self.k + 1,
                'k_inc': self.k + 2,
                'k_dec': self.k,
                'base_k_inc': self.base[self.k + 1],
                'newbase_k_inc': self.new_base[self.k + 1],
                'result': "",
                't': ', '.join(list(map(str, range(self.k + 1, self.j, -1))))
            }
            condition = self.new_base[self.k + 1] <= self.base[self.k + 1]
            params['result'] = self.document.get_step_xml('moving/R4_' + ('true' if condition else 'false'), **params)
            self.document.add_step('moving/R4_step', **params)
            if condition:
                for t in range(self.k, self.j - 1, -1):
                    self.R5(t)
                return False
            else:
                self.k += 1

    def R5(self, t: int):
        self.delta = self.new_base[t] - self.base[t]
        params = {
            't': t + 1,
            'base_t': self.base[t],
            'base_t_inc': self.base[t] + 1,
            'newbase_t': self.new_base[t],
            'delta': self.delta,
            'top_t': self.top[t],
            'top_t_dec': self.top[t] - 1,
            'l_range': ', '.join(list(map(str, range(self.top[t], self.base[t], -1))))
        }
        self.document.add_step('moving/R5', **params)

        for l in range(self.top[t], self.base[t], -1):
            params['l'] = l
            params['l_plus_delta'] = l + self.delta

            self.document.add_step('moving/R5_step', **params)
            self.memory[l + self.delta] = self.memory[l]
            self.memory[l] = 0
            self.memory_table(refresh_memory=False)

        self.base[t] = self.new_base[t]
        self.top[t] += self.delta
        params['top_t_new'] = self.top[t]
        self.document.add_step('moving/R5_end', **params)
        self.memory_table()

    def RG6(self):
        params = {
            'i': self.i + 1,
            'top_i_dec': self.top[self.i]
        }
        self.top[self.i] += 1
        params['top_i'] = self.top[self.i]

        self.document.add_step("moving/RG6", **params)
        self.memory_table(refresh_memory=False)
        self.document.add_step("moving/RG6_end", **params)
    # ===================== #
