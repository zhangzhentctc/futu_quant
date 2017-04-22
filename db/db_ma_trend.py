from db.db_basic import *


class dbop_ma_trand:
    def __init__(self):
        self.count = 0
        self.position = 0

    def dbop_store_ma_dur2(self, db_basic, ma10_val, ma20_val,cur_val, ask_val, bid_val):
        sql = "insert into dur2_trend(ma10,ma20,cur,ask,bid) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val)  + "," + str(ask_val)  + "," + str(bid_val) + ");"
        db_basic.insertMysql(sql)

    def dbop_store_ma_dur5(self, db_basic, ma10_val, ma20_val, cur_val, ask_val, bid_val):
        sql = "insert into dur5_trend(ma10,ma20,cur,ask,bid) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val)  + "," + str(ask_val)  + "," + str(bid_val) + ");"
        db_basic.insertMysql(sql)

    def dbop_read_ma_dur2(self, db_basic, time_start, time_end):
        sql = "select * from dur2_trend where time > '" + time_start + "' and time < '" + time_end + "';"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_read_ma_dur_next(self, db_basic):
        if self.position >= self.count:
            return ""
        try:
            ret = db_basic.cursor.fetchone()
        except:
            print("fetchone fail")
            return ""
        self.position += 1
        return ret
