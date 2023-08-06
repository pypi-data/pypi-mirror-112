from pyvcam import pvc
from pyvcam.camera import Camera
name = "pyvcam"
hwid = []

class instrument:
    def __init__(self,port):
        pvc.init_pvcam()  # Initialize PVCAM
        try:
            self.cam = next(Camera.detect_camera())  # Use generator to find first camera
            self.cam.open()  # Open the camera.
            if self.cam.is_open:
                print("Camera open")
        except:
            raise Exception("Error: camera not found")

    def get_frame(self, exp_time):
        return self.cam.get_frame(exp_time=exp_time)

    def roi(self, x1, x2, y1, y2):
        self.cam.roi = (x1, x2, y1, y2)

    def binning(self, xbin, ybin):
        self.cam.binning = (xbin, ybin)
