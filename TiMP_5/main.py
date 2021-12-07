from TiMP5 import Lab3


task = {
    'matrix': {
        (1, 1): 50,
        (2, 3): 20,
        (2, 1): 10,
        (4, 4): 5,
        (4, 3): -60,
        (4, 1): -30
    },
    'pivot': (2, 1)
}


if __name__ == "__main__":
    laba = Lab3(task)
    laba.run()
