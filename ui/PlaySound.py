import playsound
import time
import threading


class PlaySound(threading.Thread):
    def __init__(self):
        super(PlaySound, self).__init__()
        STOP = 0
        self.start_bear = STOP
        self.stop_lossing_bear = STOP
        self.start_bull = STOP
        self.stop_lossing_bull = STOP
        self.burst_down = STOP
        self.burst_up = STOP
        self.start_bear_path =        r"D:\quant\\test0\\futu_quant\\sounds\start_bear.wav"
        self.start_bull_path =        r"D:\quant\\test0\\futu_quant\\sounds\start_bull.wav"
        self.stop_lossing_bear_path = r"D:\quant\\test0\\futu_quant\\sounds\stop_lossing_bear.wav"
        self.stop_lossing_bull_path = r"D:\quant\\test0\\futu_quant\\sounds\stop_lossing_bull.wav"
        self.burst_down_path =        r"D:\quant\\test0\\futu_quant\\sounds\burst_down.wav"
        self.burst_up_path =          r"D:\quant\\test0\\futu_quant\\sounds\burst_up.wav"

    def play_burst_up(self):
        self.burst_up += 1

    def play_burst_down(self):
        self.burst_down += 1

    def play_stop_lossing_bull(self):
        self.stop_lossing_bull += 1

    def play_stop_lossing_bear(self):
        self.stop_lossing_bear += 1

    def play_start_bear(self):
        self.start_bear += 1

    def play_start_bull(self):
        self.start_bull += 1

    def stop_play_stop_lossing_bull(self):
        self.stop_lossing_bull = 0

    def stop_play_stop_lossing_bear(self):
        self.stop_lossing_bear = 0

    def stop_play_start_bear(self):
        self.start_bear = 0

    def stop_play_start_bull(self):
        self.start_bull = 0

    def stop_burst_up(self):
        self.burst_up = 0

    def stop_burst_down(self):
        self.burst_down = 0


    def run(self):
        while(1):
            if self.burst_up > 0:
                playsound.playsound(self.burst_up_path)
                self.burst_up -= 1

            if self.burst_down > 0:
                playsound.playsound(self.burst_down_path)
                self.burst_down -= 1

            if self.stop_lossing_bear > 0:
                playsound.playsound(self.stop_lossing_bear_path)
                self.stop_lossing_bear -= 1

            if self.stop_lossing_bull > 0:
                playsound.playsound(self.stop_lossing_bull_path)
                self.stop_lossing_bull -= 1

            if self.start_bear > 0:
                playsound.playsound(self.start_bear_path)
                self.start_bear -= 1

            if self.start_bull > 0:
                playsound.playsound(self.start_bull_path)
                self.start_bull -= 1

            time.sleep(0.2)
