import playsound
import time
import threading


class PlaySound(threading.Thread):
    def __init__(self, path = r"D:\quant\\test0\\futu_quant\Stop.wav"):
        super(PlaySound, self).__init__()
        self.path = path
        self.cnt = 0
        self.start_bear = 0
        self.start_bear_path = r"D:\quant\\test0\\futu_quant\start_bear.wav"
        self.stop_lossing_bear = 0
        self.stop_lossing_bear_path = r"D:\quant\\test0\\futu_quant\stop_lossing_bear.wav"
        self.start_bull = 0
        self.start_bull_path = r"D:\quant\\test0\\futu_quant\start_bull.wav"

    def add_cnt(self):
        self.cnt += 1

    def stop(self):
        self.cnt = 0

    def run3(self):
        while(1):
            if self.cnt > 0:
                playsound.playsound(self.path)
                self.cnt -= 1
            else:
                time.sleep(0.2)

    def play_stop_lossing_bear(self):
        self.stop_lossing_bear += 1

    def play_start_bear(self):
        self.start_bear += 1

    def play_start_bull(self):
        self.start_bull += 1

    def stop_play_stop_lossing_bear(self):
        self.stop_lossing_bear = 0

    def stop_play_start_bear(self):
        self.start_bear = 0

    def stop_play_start_bull(self):
        self.start_bull = 0

    def run(self):
        while(1):
            if self.stop_lossing_bear > 0:
                playsound.playsound(self.stop_lossing_bear_path)
                self.stop_lossing_bear -= 1

            if self.start_bear > 0:
                playsound.playsound(self.start_bear_path)
                self.start_bear -= 1

            if self.start_bull > 0:
                playsound.playsound(self.start_bull_path)
                self.start_bull -= 1

            time.sleep(0.2)
