import numpy as np

name = "software"
hwid = ["software"]


class instrument:
    def __init__(self,serial_number):
        pass

    def get_frame(self, exp_time):
        x = int((self.x2 - self.x1) / self.xbin)
        y = int((self.y2 - self.y1) / self.ybin)
        return np.random.rand(x, y)

    def roi(self, x1, x2, y1, y2):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2

    def binning(self, xbin, ybin):
        self.xbin, self.ybin = (xbin, ybin)
