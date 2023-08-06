from K10CR1.k10cr1 import K10CR1

name = "K10CR1"
hwid = ["0403:FAF0"]


# k10cr1 = { git = 'https://github.com/QuantumQuadrate/k10cr1' }
# add line to pyproject.toml or package

# since the rotator api is based off K10CR1, this is probably the most boring file you'll ever see
def find_ports(type):
    return ["55001000", "55114554", "55114654"]
    # more or less documentation on finding the rotator


class instrument:
    def __init__(self, port):
        self.rotator = K10CR1(port.serial_number)
        self.home()

    def home(self):
        self.rotator.home()

    def move_abs(self, value):
        self.rotator.moveabs(value)

    def move_rel(self, val_dif):
        self.rotator.moverel(val_dif)
