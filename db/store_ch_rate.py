from db.db_ma_trend import *
import threading
import time


class store_ch_rate(threading.Thread):
    def __init__(self, zma_str):
        super(store_ch_rate, self).__init__()
        self.zma_str = zma_str


    def run(self):
        print("Run store ch rate")
        db = MySQLCommand("localhost", 3306, "root", "123456", "trend2")
        print("connect DB")
        db.connectMysql()
        print("Init")
        op = dbop_ma_trand()
        while(1):
            try:
                cur = self.zma_str.cur
                cur_gap_5s = self.zma_str.cur_gap_5s
                cur_gap_10s = self.zma_str.cur_gap_10s
                cur_gap_20s = self.zma_str.cur_gap_20s
            except:
                time.sleep(0.5)
                continue
            print("Get numbers")
            op.dbop_add_ch_rates(db, cur, cur_gap_5s, cur_gap_10s, cur_gap_20s)
            time.sleep(0.5)
