import elliptec
name = "elliptec"
hwid = []
def find_ports():
    return elliptec.find_ports()
    # more or less documentation on finding the rotator


class instrument:
    def __init__(self, i):
        ports = elliptec.find_ports()
        for port in ports:
            if port.serial_number == i:
                self.rotator = elliptec.Motor(port.device)
                self.home()
        self.max_degree = 180
        self.min_degree = -180
        '''
        elif type == "thorlabs_apt":
            rotator = apt.Motor(i[1])
            rotator.set_move_home_parameters(2, 1, 10, 0)
            rotator.set_velocity_parameters(0, 10, 10)
            rotator.move_home()
            return rotator
        '''

    def home(self):
        self.degree = 0
        self.rotator.do_("home")

    def move_abs(self, value):
        val_dif = (value - self.degree) % 360
        self.move_rel(val_dif)

    def move_rel(self, val_dif):
        new_val = self.degree + val_dif
        while new_val > self.max_degree:
            new_val -= 360
            val_dif -= 360
        while new_val < self.min_degree:
            new_val += 360
            val_dif += 360
        val = self.rotator.deg_to_hex(abs(val_dif))
        self.rotator.set_('stepsize', val)
        if val_dif > 0:
            self.rotator.do_("forward")
            self.degree = (self.degree + val_dif)
        elif val_dif < 0:
            self.rotator.do_("backward")
            self.degree = (self.degree + val_dif)
        else:
            print("No change, moving 0 degrees")
