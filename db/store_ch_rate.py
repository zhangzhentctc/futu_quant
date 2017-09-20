from db.db_ma_trend import *
import threading
import time


class store_ch_rate(threading.Thread):
    def __init__(self, zma_str):
        super(store_ch_rate, self).__init__()
        self.zma_str = zma_str


    def run(self):

        db = MySQLCommand("localhost", 3306, "root", "123456", "trend2")
        db.connectMysql()
        op = dbop_ma_trand()
        while(1):
            if self.zma_str.running == 1:
                try:
                    cur = self.zma_str.cur
                    cur_gap_5s = self.zma_str.cur_gap_5s
                    cur_gap_10s = self.zma_str.cur_gap_10s
                    cur_gap_20s = self.zma_str.cur_gap_20s
                    MA10_cur = self.zma_str.MA10_cur
                    MA20_cur = self.zma_str.MA20_cur
                    deltaMA10_ma3 = self.zma_str.deltaMA10_ma3
                    deltaMA20_ma3 = self.zma_str.deltaMA20_ma3
                except:
                    time.sleep(0.5)
                    continue
                op.dbop_add_standard_quo(db, cur, MA10_cur, MA20_cur, deltaMA10_ma3, deltaMA20_ma3)
                op.dbop_add_ch_rates(db, cur, cur_gap_5s, cur_gap_10s, cur_gap_20s)
                time.sleep(0.5)
            else:
                time.sleep(0.5)

