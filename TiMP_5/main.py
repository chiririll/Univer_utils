from TiMP5 import Lab5

import utils
from element import Element

task = {
    'matrix': {
        (1, 1): Element(50),
        (2, 3): Element(20),
        (2, 1): Element(10),
        (4, 4): Element(5),
        (4, 3): Element(-60),
        (4, 1): Element(-30)
    },
    'pivot': (2, 1)
}


if __name__ == "__main__":
    utils.clear_folder("output/images")

    for cords, el in task['matrix'].items():
        el.find_links(cords, task['matrix'])

    import drawer
    drawer.draw('test', task['matrix'], [])

    # laba = Lab5(task)
    # laba.run()
