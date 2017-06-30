import playsound
import time

class PlaySound:
    def __init__(self, path = r"D:\quant\\test0\\futu_quant\Stop.wav"):
        self.path = path
        self.status = 0

    def playSound(self):
        if self.status == 0:
            self.status = 1
            playsound.playsound(self.path)
            self.status = 0
        else:
            time.sleep(5)
            self.status = 1
            playsound.playsound(self.path)
            self.status = 0

    def check_status(self):
        return self.status


