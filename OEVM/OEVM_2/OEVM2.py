from word_parser import Document
import utils


class Laba2:
    def __init__(self, var, name, function, filename='out'):
        self.document = Document(f"output/{filename}.doc")

        self.var = var
        self.name = name
        self.function = function
        self.max_intervals = []

    def run(self):
        self.CCNF()
        self.intervals()
        self.decrease_func()
        self.generate_table()

    def CCNF(self):
        self.document.add_step('ccnf', function=list(map(utils.get_bin, self.function)), utils=utils)

    def intervals(self):
        intervals = []
        max_intervals = []

        last_res = []
        for i in range(4):
            res = self.function if i == 0 else last_res.copy()
            if len(res) == 0:
                break

            last_res.clear()

            for interval, desc in utils.get_max_intervals(res):
                if desc:
                    last_res.append(interval)
                elif interval not in max_intervals:
                    max_intervals.append(interval)

            for interval in res:
                if interval not in intervals:
                    intervals.append(f'{interval:04b}' if type(interval) is int else interval)

        self.max_intervals = max_intervals
        self.document.add_step('intervals', intervals=intervals, max_intervals=max_intervals)

    def decrease_func(self):
        self.document.add_step('decreased_func', func_index='s', function=self.max_intervals)

    def generate_table(self):
        results = []
        for part in self.function:
            ltrs = []
            for i, interval in enumerate(self.max_intervals):
                if utils.check_interval(interval, part) == '1':
                    ltrs.append(utils.get_ltr_by_index(i))
            results.append(ltrs)

        context = {
            'function': self.function,
            'max_intervals': self.max_intervals,
            'results': results
        }

        self.document.add_step('table', **context)
