import playsound
import time
import threading

STOP = 0


class PlaySound(threading.Thread):
    def __init__(self):
        super(PlaySound, self).__init__()

        self.start_bear =        STOP
        self.stop_lossing_bear = STOP
        self.stop_lossing_bear_inst= STOP
        self.start_bull =        STOP
        self.stop_lossing_bull = STOP
        self.burst_down =        STOP
        self.burst_up =          STOP
        self.morning_warn =      STOP
        self.no_trend =          STOP
        self.warn_bull_revover = STOP

        self.start_bear_path =        r"D:\quant\\test0\\futu_quant\\sounds\start_bear.wav"
        self.start_bull_path =        r"D:\quant\\test0\\futu_quant\\sounds\start_bull.wav"
        self.stop_lossing_bear_path = r"D:\quant\\test0\\futu_quant\\sounds\stop_lossing_bear.wav"
        self.stop_lossing_bear_inst_path = r"D:\quant\\test0\\futu_quant\\sounds\stop_lossing_bear_inst.wav"
        self.stop_lossing_bull_path = r"D:\quant\\test0\\futu_quant\\sounds\stop_lossing_bull.wav"
        self.burst_down_path =        r"D:\quant\\test0\\futu_quant\\sounds\burst_down.wav"
        self.burst_up_path =          r"D:\quant\\test0\\futu_quant\\sounds\burst_up.wav"
        self.morning_warn_path =      r"D:\quant\\test0\\futu_quant\\sounds\morning_warn.wav"
        self.no_trend_path =          r"D:\quant\\test0\\futu_quant\\sounds\no_trend.wav"
        self.warn_bull_revover_path = r"D:\quant\\test0\\futu_quant\\sounds\warn_bull_revover.wav"

# PLAY Signal
    def play_burst_up(self):
        self.burst_up += 1

    def play_burst_down(self):
        self.burst_down += 1

    def play_stop_lossing_bull(self):
        self.stop_lossing_bull += 1

    def play_stop_lossing_bear(self):
        self.stop_lossing_bear += 1

    def play_stop_lossing_bear_inst(self):
        self.stop_lossing_bear_inst += 1

    def play_start_bear(self):
        self.start_bear += 1

    def play_start_bull(self):
        self.start_bull += 1

    def play_morning_warn(self):
        self.morning_warn += 1

    def play_no_trend(self):
        self.no_trend += 1

    def play_warn_bull_recover(self):
        self.warn_bull_revover += 1



# STOP Signal
    def stop_play_stop_lossing_bull(self):
        self.stop_lossing_bull = STOP

    def stop_play_stop_lossing_bear(self):
        self.stop_lossing_bear = STOP
        self.stop_lossing_bear_inst = STOP

    def stop_play_start_bear(self):
        self.start_bear = STOP

    def stop_play_start_bull(self):
        self.start_bull = STOP

    def stop_burst_up(self):
        self.burst_up = STOP

    def stop_burst_down(self):
        self.burst_down = STOP

    def stop_play_morning_warn(self):
        self.morning_warn = STOP

    def stop_play_no_trend(self):
        self.no_trend = STOP

    def stop_play_warn_bull_recover(self):
        self.warn_bull_revover = STOP

    def run(self):
        while(1):
            if self.burst_up != STOP:
                playsound.playsound(self.burst_up_path)
                self.burst_up -= 1

            if self.burst_down != STOP:
                playsound.playsound(self.burst_down_path)
                self.burst_down -= 1

            if self.stop_lossing_bear != STOP:
                playsound.playsound(self.stop_lossing_bear_path)
                self.stop_lossing_bear -= 1

            if self.stop_lossing_bear_inst != STOP:
                playsound.playsound(self.stop_lossing_bear_inst_path)
                self.stop_lossing_bear_inst -= 1

            if self.stop_lossing_bull != STOP:
                playsound.playsound(self.stop_lossing_bull_path)
                self.stop_lossing_bull -= 1

            if self.start_bear != STOP:
                playsound.playsound(self.start_bear_path)
                self.start_bear -= 1

            if self.start_bull != STOP:
                playsound.playsound(self.start_bull_path)
                self.start_bull -= 1

            if self.no_trend != STOP:
                playsound.playsound(self.no_trend_path)
                self.no_trend -= 1

            if self.morning_warn != STOP:
                playsound.playsound(self.morning_warn_path)
                self.morning_warn -= 1

            if self.warn_bull_revover != STOP:
                playsound.playsound(self.warn_bull_revover_path)
                self.warn_bull_revover -= 1

            time.sleep(0.2)
