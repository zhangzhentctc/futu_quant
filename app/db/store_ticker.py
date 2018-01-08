from app.db.db_ticker import *
import threading
import time
import json


class store_ticker(threading.Thread):
    def __init__(self, ticker_buff, bat_num = 5):
        super(store_ticker, self).__init__()
        self.ticker_buff = ticker_buff
        self.bat_num = bat_num

    def fetch_data(self):
        self.ticker_buff.open_mmap()
        ret, s = self.ticker_buff.buffer_read()
        self.val = []
        if s != "":
            sm_data = json.loads(s)
            list = sm_data["data"]
            if len(list) != 0:
                for i in range(0, self.bat_num):
                    self.val.append(list.pop(0))
                    if len(list) == 0:
                        break

            if len(list) == 0:
                json_str = ""
            else:
                data = {}
                data["data"] = list
                json_str = json.dumps(data)

            self.ticker_buff.buffer_reset()
            self.ticker_buff.buffer_write(json_str)
            self.ticker_buff.close_mmap()

    def process_val(self):
        while self.val != []:
            row = self.val.pop(0)
            self.op.dbop_insert_ticker_sequence(self.db, row[0], row[1], row[2], row[3], row[4])

    def run(self):

        self.db = MySQLCommand("localhost", 3306, "root", "123456", "ticker")
        self.db.connectMysql()
        self.op = db_ticker()

        while True:
            if self.ticker_buff.mutex_lock.acquire(1):
                self.fetch_data()
                self.ticker_buff.mutex_lock.release()
                self.process_val()
            time.sleep(0.5)

