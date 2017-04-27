from db.db_basic import *


class dbop_ma_trand:
    def __init__(self):
        self.count = 0
        self.position = 0

    def dbop_store_ma_dur2(self, db_basic, ma10_val, ma20_val,cur_val, ask_val, bid_val, ask_p_val, bid_p_val):
        sql = "insert into dur2_trend(ma10,ma20,cur,ask,bid, p_ask, p_bid) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val)  + "," + str(ask_val)  + "," + str(bid_val) + "," + str(ask_p_val) + "," + str(bid_p_val) + ");"
        db_basic.insertMysql(sql)

    def dbop_store_ma_dur5(self, db_basic, ma10_val, ma20_val, cur_val, ask_val, bid_val, ask_p_val, bid_p_val):
        sql = "insert into dur5_trend(ma10,ma20,cur,ask,bid, p_ask, p_bid) values(" + str(ma10_val) + "," + str(ma20_val) + "," + str(cur_val)  + "," + str(ask_val)  + "," + str(bid_val) + "," + str(ask_p_val) + "," + str(bid_p_val) + ");"
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

    def dbop_add_day_data(self, db_basic,id,cur,time, zma10,zma20, delta_zma10, delta_zma20, delta_zma10_ma60, delta_zma20_ma60, ratio, zma_gap, zma_gap_ratio, delta_zma20_ma60_ratio, zma10_ratio, zma20_ratio, zma20_ratio_ratio):
        sql = "insert into day_data(id,cur,time, zma10,zma20, delta_zma10, delta_zma20, delta_zma10_ma60, delta_zma20_ma60, ratio, zma_gap, zma_gap_ratio, delta_zma20_ma60_ratio, zma10_ratio, zma20_ratio, zma20_ratio_ratio) values(" + \
              str(id) + "," + str(cur) + ", '" + str(time) + "' ," + str(zma10) + "," + str(zma20) + "," + \
              str(delta_zma10) + "," + str(delta_zma20) + "," +  str(delta_zma10_ma60) + "," + str(delta_zma20_ma60) + "," + str(ratio) + "," + str(zma_gap) + "," + str(zma_gap_ratio) + "," + str(delta_zma20_ma60_ratio) + "," + str(zma10_ratio) + "," + str(zma20_ratio) + "," + str(zma20_ratio_ratio) + ");"
        db_basic.insertMysql(sql)

    def dbop_read_day_data(self, db_basic, time_start, time_end):
        sql = "select * from day_data where time > '" + time_start + "' and time < '" + time_end + "';"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_read_day_data_next(self, db_basic):
        if self.position >= self.count:
            return ""
        try:
            ret = db_basic.cursor.fetchone()
        except:
            print("fetchone fail")
            return ""
        self.position += 1
        return ret