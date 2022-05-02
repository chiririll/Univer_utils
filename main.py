import json

from Shared.Classes import Executor
import OIB
import MIS
from TiMP import TiMP_1


def make_all(laba_class, tasks: list[str] | str):
    with open("students.json", 'r', encoding="UTF-8") as f:
        students = json.load(f)

    if type(tasks) is str:
        # Load from file
        with open("OIB/Laba_6/variants.json", 'r', encoding="UTF-8") as f:
            tasks = json.load(f)

    for student, var in students.items():
        print(f"Generating {laba_class.laba['subject']}/{laba_class.laba['name']} for variant {var}...")
        laba = laba_class(tasks[str(var)], executor=Executor(student, var))
        laba.run()

def make_OIB():
    # Criticality
    test_var = {
        'executor': Executor(),
        'task': [
            # Server, PC-1, PC-2, PC-3
            [69, 4, 14, 14],    # Privacy
            [74, 16, 21, 12],   # Integrity
            [53, 12, 15, 12]    # Availability
        ]
    }

    make_all(OIB.Laba6, "OIB/Laba_6/variants.json")


def make_MIS():
    laba = MIS.Laba2()
    laba.run()


def TiMP1():
    TiMP_1.main()


if __name__ == "__main__":
    make_MIS()
