from db.db_basic import *
import time
from strategies.zma.feature_data_pkg import *

class db_ml:
    def __init__(self):
        self.count = 0
        self.position = 0

    def dbop_agancy_begin(self, db_basic):
        db_basic.agency_begin()

    def dbop_agancy_commit(self, db_basic):
        db_basic.agency_commit()

    def dbop_agancy_rollback(self, db_basic):
        db_basic.agency_rollback()

###########Oprations on table onebar
    def dbop_insert_raw_data(self, db_basic, k_start, k_end, k_high, k_low, ma5, ma10, ma20, ret, day, num):
        sql = "insert into onekbar(day,num,k_start,k_end,k_high,k_low,ma5,ma10,ma20,ret) values(" + \
              str(day) + "," + str(num) + "," + str(k_start) + "," + str(k_end) + "," + str(k_high) + "," + str(k_low) + "," + \
              str(ma5) + "," + str(ma10) + "," + str(ma20) + "," + str(ret) + ");"
        ret = db_basic.insertMysql(sql)
        return ret


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
        ret = db_basic.insertMysql(sql)
        #print(sql)
        return ret

###########Oprations on table samples
    ### k_vals should be a 4 * 7 matrix
    def dbop_insert_sample(self, db_basic, day, num, k_vals):
        sql = "insert into samples(day,num"
        print(k_vals)
        for i in range(1, 8):
            sql += ",k_end_" + str(i) + ",ma5_" + str(i) + ",ma10_" + str(i) + ",ma20_" + str(i)

        sql += ")values(" + \
              str(day) + "," + str(num)

        for i in range(0, 7):
            for j in range(0, 4):
                sql += "," + str(k_vals[i][j])

        sql += ");"

        ret = db_basic.insertMysql(sql)
        return ret

    def dbop_get_sample(self, db_basic):
        sql = "select * from samples;"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_get_sample_next(self, db_basic):
        if self.position >= self.count:
            return ""
        try:
            ret = db_basic.cursor.fetchone()
        except:
            print("fetchone fail")
            return ""
        self.position += 1
        return ret