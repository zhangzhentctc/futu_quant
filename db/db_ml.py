from db.db_basic import *
import time
from strategies.zma.feature_data_pkg import *

class dbop_ml:
    def __init__(self):
        self.count = 0
        self.position = 0


    def dbop_insert_raw_data(self, db_basic, k_start, k_end, k_high, k_low, ma5, ma10, ma20, ret, day, num):
        sql = "insert into onekbar(day,num,k_start,k_end,k_high,k_low,ma5,ma10,ma20,ret) values(" + \
              str(day) + "," + str(num) + "," + str(k_start) + "," + str(k_end) + "," + str(k_high) + "," + str(k_low) + "," + \
              str(ma5) + "," + str(ma10) + "," + str(ma20) + "," + str(ret) + ");"
        db_basic.insertMysql(sql)

    def dbop_get_day_data(self, db_basic, day):
        sql = "select * from onekbar where day = " + str(day) + " order by num;"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_get_day_data_next(self, db_basic):
        if self.position >= self.count:
            return ""
        try:
            ret = db_basic.cursor.fetchone()
        except:
            print("fetchone fail")
            return ""
        self.position += 1
        return ret

    def dbop_update_day_data_trade_mark(self, db_basic, ret, day, num):
        sql = "update onekbar set ret = " + str(ret) + " where day = " + str(day) + " and num = " + str(num) + ";"
        db_basic.insertMysql(sql)


