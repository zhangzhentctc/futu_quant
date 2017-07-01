import playsound
import time
import threading


class PlaySound(threading.Thread):
    def __init__(self, path = r"D:\quant\\test0\\futu_quant\Stop.wav"):
        super(PlaySound, self).__init__()
        self.path = path
        self.status = 0
        self.cnt = 0

    def check_status(self):
        return self.status

    def add_cnt(self):
        self.cnt += 1

    def stop(self):
        self.cnt = 0

    def run(self):
        while(1):
            if self.cnt > 0:
                playsound.playsound(self.path)
                self.cnt -= 1;
            else:
                time.sleep(0.2)


