from app.db.db_ticker import *
import pandas as pd


class ticker_handler:
    def __init__(self, date = '2018-01-09'):
        self.length = -1
        self.date = date
        self.start_ptr = -1
        self.start_time_s = 0
        self.end_ptr = -1
        self.end_time_s = 0
        self.noon_rest_time = '12:00:00'

    def init_db(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "ticker")
        self.db.connectMysql()
        self.dbop = db_ticker()

## date,time,price,volume,direction,sequence

    def import_tickers_from_db(self):
        count = self.dbop.dbop_get_day_ticker(self.db, self.date)
        if count == 0:
            print("Ticker Data Does Not Exist")
            return -1
        data = []
        for i in range(0, count):
            line = self.dbop.dbop_get_day_ticker_next(self.db)
            time_seconds = self.__parse_time(line[1])
            data.append({
                "time": time_seconds,
                "price": line[2],
                "volume": line[3],
                "direction": line[4],
                "sequence": line[5],
                "real_time": line[1]
            })


        self.tickers = pd.DataFrame(data, columns=[
                "time",
                "price",
                "volume",
                "direction",
                "sequence",
                "real_time"
        ])

        self.length = len(self.tickers.index)
        self.start_ptr = 0
        self.start_time_s = self.tickers["time"][0]
        self.end_ptr = 0
        self.end_time_s = self.start_time_s
        self.noon_rest_time_s = self.__parse_time(self.noon_rest_time)
        return

##09:34:23
    def set_start(self, start_time):
        ret = -1
        self.start_time_s = self.__parse_time(start_time)
        for i in range(0, self.length):
            if self.tickers["time"][i] >= self.start_time_s:
                self.start_ptr = i
                ret = 0
                break
        if ret == -1:
            print("Set Start Pointer Fail")
            return
        self.end_ptr = self.start_ptr
        self.end_time_s = self.start_time_s
        self.move_end_ptr(60)
        return

    def move_end_ptr(self, seconds):
        ret = -1
        if self.end_time_s + seconds + 1 > self.noon_rest_time_s and \
           self.start_time_s <= self.noon_rest_time_s:
            dest_time_s = self.end_time_s + seconds + 1 + 3600
        else:
            dest_time_s = self.end_time_s + seconds + 1

        for i in range(self.end_ptr, self.length):
            if self.tickers["time"][i] >= dest_time_s:
                self.end_ptr = i - 1
                ret = 0
                break
        if ret == -1:
            print("Move End Pointer Fail")
            return
        self.end_time_s = dest_time_s - 1
        return

    def gen_data(self):
        self.price_l = []
        self.buy_l = []
        self.neul_l = []
        self.sell_l = []
        for i in range(self.start_ptr, self.end_ptr + 1):
            price = int(self.tickers["price"][i])
            volume = int(self.tickers["volume"][i])
            direction = self.tickers["direction"][i]

            have_p = False
            for p in self.price_l:
                if p == price:
                    have_p = True
                    break

            if have_p == False:
                self.price_l.append(price)
                self.buy_l.append(0)
                self.neul_l.append(0)
                self.sell_l.append(0)

            # Insert Vol
            for pos in range(0, len(self.price_l)):
                if self.price_l[pos] == price:
                    if direction == "TT_BUY":
                        self.buy_l[pos]  += volume
                    if direction == "TT_NEUTRAL":
                        self.neul_l[pos] += volume
                    if direction == "TT_SELL":
                        self.sell_l[pos] += volume

            # Sort by price
            for i in range(1, len(self.price_l)):
                for j in range(0, i):
                    if self.price_l[i] < self.price_l[j]:
                        ##exchange
                        tmp = self.price_l[j]
                        self.price_l[j] = self.price_l[i]
                        self.price_l[i] = tmp

                        tmp = self.buy_l[j]
                        self.buy_l[j] = self.buy_l[i]
                        self.buy_l[i] = tmp

                        tmp = self.neul_l[j]
                        self.neul_l[j] = self.neul_l[i]
                        self.neul_l[i] = tmp

                        tmp = self.sell_l[j]
                        self.sell_l[j] = self.sell_l[i]
                        self.sell_l[i] = tmp

        return

    def get_start_time(self):
        return self.tickers["real_time"][self.start_ptr]

    def get_end_time(self):
        return self.tickers["real_time"][self.end_ptr]

    def __parse_time(self, time_):
        time_list = time_.split(":")
        time_second = int(time_list[0]) * 3600 + \
                      int(time_list[1]) * 60 + \
                      int(time_list[2])
        return time_second

