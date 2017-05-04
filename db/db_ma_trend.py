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

    # "No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio",
    def dbop_add_day_data(self, db_basic, id, cur, time, zma10, zma20, zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap, zma_gap_ratio, zma_gap_ratio_ratio, zma_gap_ratio_ratio_r, trade_mark):
        sql = "insert into day_data_new2(id,cur,time, zma10,zma20, zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap, zma_gap_ratio, zma_gap_ratio_ratio, zma_gap_ratio_ratio_r, trade_mark) values(" + \
              str(id) + "," + str(cur) + ", '" + str(time) + "' ," + str(zma10) + "," + str(zma20) + "," + \
              str(zma10_ratio) + "," + str(zma20_ratio) + "," + str(zma10_ratio_ratio) + "," + str(zma20_ratio_ratio) + "," + \
              str(zma_gap) + "," + str(zma_gap_ratio) + "," + str(zma_gap_ratio_ratio) + "," + str(zma_gap_ratio_ratio_r) + "," + str(trade_mark) + ");"
        db_basic.insertMysql(sql)

    def dbop_read_day_data(self, db_basic, time_start, time_end):
        sql = "select * from day_data_new2 where time > '" + time_start + "' and time < '" + time_end + "';"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_update_day_data_trade_mark(self, db_basic, id, trade_mark):
        sql = "update day_data_new2 set trade_mark = " + str(trade_mark) + "where id = " + str(id) + ";"
        db_basic.insertMysql(sql)



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
