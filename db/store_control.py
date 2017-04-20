from db.db_ma_trend import *
import threading
import time


class store_control(threading.Thread):
    def __init__(self, detectMATrend, detectMATrend5, ma):
        super(store_control, self).__init__()
        self.detectMATrend = detectMATrend
        self.detectMATrend5 = detectMATrend5
        self.ma = ma

    def run(self):
        db = MySQLCommand("localhost", 3306, "root", "123456", "trend")
        db.connectMysql()
        op = dbop_ma_trand()
        while(1):
            ma10_rate, ma20_rate = self.detectMATrend.get_ma_ch_rate()
            if abs(ma10_rate) > 100 or abs(ma20_rate) > 100:
                continue
            ma10_rate = round(ma10_rate, 3)
            ma20_rate = round(ma20_rate, 3)
            cur_val = self.detectMATrend.get_cur_val()
            ask, bid = self.ma.get_get_ask_bid()
            op.dbop_store_ma_dur2(db, ma10_rate, ma20_rate, cur_val, ask, bid)
            ma10_rate_5, ma20_rate_5 = self.detectMATrend5.get_ma_ch_rate()
            if abs(ma10_rate_5) > 100 or abs(ma20_rate_5) > 100:
                continue
            ma10_rate_5 = round(ma10_rate_5, 3)
            ma20_rate_5 = round(ma20_rate_5, 3)
            cur_val = self.detectMATrend.get_cur_val()
            op.dbop_store_ma_dur5(db, ma10_rate_5, ma20_rate_5, cur_val, ask, bid)
            time.sleep(0.5)
