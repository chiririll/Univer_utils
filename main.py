import json

import OIB
from Shared.Classes import Executor
from TiMP import TiMP_1


def OIS():
    with open("OIB/Laba_6/variants.json", 'r', encoding="UTF-8") as f:
        tasks = json.load(f)

    with open("students.json", 'r', encoding="UTF-8") as f:
        students = json.load(f)

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

    for student, var in students.items():
        print(f"Generating OIB.6 for variant {var}...")
        laba = OIB.Laba6(tasks[str(var)], executor=Executor(student, var))
        laba.run()


def TiMP1():
    TiMP_1.main()


if __name__ == "__main__":
    OIS()
