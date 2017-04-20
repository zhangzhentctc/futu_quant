from db.db_basic import *


class dbop_ma_trand:
    def __init__(self):
        pass

    def dbop_store_ma_dur2(self, db_basic, ma10_val, ma20_val,cur_val):
        sql = "insert into dur2_trend(ma10,ma20,cur) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val) + ");"
        db_basic.insertMysql(sql)

    def dbop_store_ma_dur5(self, db_basic, ma10_val, ma20_val, cur_val):
        sql = "insert into dur5_trend(ma10,ma20,cur) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val) + ");"
        db_basic.insertMysql(sql)
