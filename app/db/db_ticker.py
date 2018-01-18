from db.db_basic import *
import time
from strategies.zma.feature_data_pkg import *

class db_ticker:
    def __init__(self):
        self.count = 0
        self.position = 0

    def dbop_agancy_begin(self, db_basic):
        db_basic.agency_begin()

    def dbop_agancy_commit(self, db_basic):
        db_basic.agency_commit()

    def dbop_agancy_rollback(self, db_basic):
        db_basic.agency_rollback()

###########Oprations on table ticker
    def dbop_insert_ticker_sequence(self, db_basic, time_, price, volume, direction, sequence):
        #2017-12-15
        #13:58:56
        time_tl = time_.split(" ")
        sql = "insert into ticker20180112(date,time,price,volume,direction,sequence) values(" + \
              "'" + str(time_tl[0]) + "'" + "," + \
              "'" + str(time_tl[1]) + "'" + "," + \
              str(price) + "," + \
              str(volume) + "," + \
              "'" + str(direction) + "'" + "," + \
              "'" + str(sequence)  + "'" + ");"
        #print(sql)
        ret = db_basic.insertMysql(sql)
        return 1


    def dbop_get_day_ticker(self, db_basic, day):
        sql = "select * from ticker order by sequence;"
        #sql = "select * from ticker where date = " + str(day) + " order by sequence;"
        self.count = db_basic.queryMysql(sql)
        return self.count

    def dbop_get_day_ticker_next(self, db_basic):
        if self.position >= self.count:
            return ""
        try:
            ret = db_basic.cursor.fetchone()
        except:
            print("fetchone fail")
            return ""
        self.position += 1
        return ret
