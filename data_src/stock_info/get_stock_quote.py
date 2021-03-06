from openft.open_quant_context import *
import threading
import time


class get_stock_quote(threading.Thread):
    def __init__(self, qc,  bull_code, bear_code, stock_code="HK_FUTURE.999010", cycle= 0.25):
        super(get_stock_quote, self).__init__()
        self.__quote_ctx = qc
        self.stock_code_list = [stock_code, bull_code, bear_code]
        self.cur_stock_quoto = 0
        self.cur_stock_quoto_delta = 0
        self.cur_stock_quoto_index = "last_price"
        self.cur_stock_quoto_volume = 0
        self.cur_stock_quoto_volume_delta = 0
        self.cur_stock_quoto_volume_index = "volume"
        self.data_time = ""
        self.data_time_index = "data_time"
        self.amplitude_index = "amplitude"
        self.cur_amplitude = 0
        self.subscribe_trail = 3
        self.refresh = cycle
        self.ready = 0
        self.deltaMA20_cur = 0
        self.deltaMA20_ma3 = 0
        self.deltaMA20_ma5 = 0
        self.k_num = 56

        ### For Quote
        self.bull_bid = -1
        self.bull_ask = -1
        self.bear_bid = -1
        self.bear_ask = -1
        self.bull_bid_seller = -1
        self.bull_ask_seller = -1
        self.bear_bid_seller = -1
        self.bear_ask_seller = -1

        self.MA20_vol = 0
        self.MA20_vol_last = 0
        self.vol_last = 0
        self.vol_now = 0

        self.MA10h_now = 0
        self.ma5_list = []
        self.ma5_list_reverse = []
        self.ma3_list = []
        self.onemk =[]

    def subscribe_stock(self, type):
        # subscribe "QUOTE"
        for stk_code in self.stock_code_list:
            ret_status, ret_data = self.__quote_ctx.subscribe(stk_code, type)
            if ret_status != RET_OK:
                print("%s %s: %s" % (stk_code, "QUOTE", ret_data))
                return RET_ERROR, ret_data
        ret_status, ret_data = self.__quote_ctx.query_subscription()
        if ret_status == RET_ERROR:
            print(ret_status)
            return RET_ERROR, ret_data
        return RET_OK, ret_data

    def get_rt_ticker(self):
        ret_status, ret_data = self.__quote_ctx.get_rt_ticker("HK_FUTURE.999010", num=500)
        if ret_status == RET_ERROR:
            print("Ticker Error: ", ret_data)
            return RET_ERROR
        print("Ticker", ret_data)

    def get_cur_stock_quoto(self):
        ret_status, ret_data = self.__quote_ctx.get_stock_quote(self.stock_code_list)
        if ret_status == RET_ERROR:
            return RET_ERROR
        quote_table = ret_data
        #print("Quoto", ret_data)


        val = quote_table[self.cur_stock_quoto_index][0]
        cur_time = quote_table[self.data_time_index][0]
        cur_amplitude = quote_table[self.amplitude_index][0]
        cur_volume = quote_table[self.cur_stock_quoto_volume_index][0]


        if val == 0:
            print("Get Val = 0 skip")
            return RET_ERROR

        if self.cur_stock_quoto_volume == 0:
            self.cur_stock_quoto_volume = cur_volume
        else:
            self.cur_stock_quoto_volume_delta = cur_volume - self.cur_stock_quoto_volume
            self.cur_stock_quoto_volume = cur_volume

        if self.cur_stock_quoto == 0:
            self.cur_stock_quoto = val
        else:
            self.cur_stock_quoto_delta = val - self.cur_stock_quoto
            self.cur_stock_quoto = val


        self.data_time = cur_time
        self.cur_amplitude = cur_amplitude
        return RET_OK

    def find_seller(self, ask_or_bid, seller_ident):
        max_val = seller_ident * 1000000
        count = 0
        pos = -1
        for item in ask_or_bid:
            if item[1] > max_val:
                pos = count
                break
            count += 1
        return pos

    def get_ask_bid(self):
        seller_ident = 10

        ret_status, ret_data = self.__quote_ctx.get_order_book(self.stock_code_list[1])
        if ret_status == RET_ERROR:
            return RET_ERROR

        self.bull_bid = ret_data["Bid"][0][0]
        self.bull_ask = ret_data["Ask"][0][0]

        pos = self.find_seller(ret_data["Bid"], seller_ident)
        if pos != -1:
            self.bull_bid_seller = ret_data["Bid"][pos][0]
        else:
            self.bull_bid_seller = -1

        pos = self.find_seller(ret_data["Ask"], seller_ident)
        if pos != -1:
            self.bull_ask_seller = ret_data["Ask"][pos][0]
        else:
            self.bull_ask_seller = -1

        ret_status, ret_data = self.__quote_ctx.get_order_book(self.stock_code_list[2])
        if ret_status == RET_ERROR:
            return RET_ERROR

        self.bear_bid = ret_data["Bid"][0][0]
        self.bear_ask = ret_data["Ask"][0][0]

        pos = self.find_seller(ret_data["Bid"], seller_ident)
        if pos != -1:
            self.bear_bid_seller = ret_data["Bid"][pos][0]
        else:
            self.bear_bid_seller = -1

        pos = self.find_seller(ret_data["Ask"], seller_ident)
        if pos != -1:
            self.bear_ask_seller = ret_data["Ask"][pos][0]
        else:
            self.bear_ask_seller = -1

        return RET_OK


    def get_data_time(self):
        return self.data_time

    def get_stock_quoto(self):
        return self.cur_stock_quoto

    def get_stock_amplitude(self):
        return self.cur_amplitude

    def get_1mK_line(self):
        ret = 0
        try:
            table = self.ma_1m_table
            ret = 1
        except:
            ret = 0
            table = []
        return ret, table

    def get_ma_1m(self, number):

        stock_code_list = [self.stock_code_list[0]]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    return
                kline_table = ret_data
#                print(kline_table)
                # Make Data List
                self.ma_1m_table = kline_table
                return self.ma_1m_table



    def get_ma_60m(self, number=10):

        stock_code_list = [self.stock_code_list[0]]
        sub_type_list = ["K_60M"]

        for code in stock_code_list:
            for ktype in ["K_60M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    return
                kline_table = ret_data
                self.ma_60m_table = kline_table
                return self.ma_60m_table

    def cal_vol_ma(self):
        K_NO = self.k_num
        try:
            kline = self.ma_1m_table
        except:
            return

        tmp = 0
        for i in range(0, 20):
            tmp += int(kline.iloc[K_NO - 1 - i, 6])
        MA20_vol = tmp/20
        self.MA20_vol = round(MA20_vol, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += int(kline.iloc[K_NO - 2 - i, 6])
        MA20_vol_last = tmp/20
        self.MA20_vol_last = round(MA20_vol_last, 2)


        self.vol_last = int(kline.iloc[K_NO - 2, 6])
        self.vol_now = int(kline.iloc[K_NO - 1, 6])
        #print("VOL MA20:", self.MA20_vol, "Last:", self.vol_last, " now:", self.vol_now)

        return

    def get_ma20_vol(self):
        return self.MA20_vol

    def get_ma20_vol_last(self):
        return self.MA20_vol_last

    def get_vol_last(self):
        return self.vol_last

    def get_vol_now(self):
        return self.vol_now

    # From new to old
    def cal_MA3_list(self):

        K_NO = self.k_num
        ma_length = 3
        list_count = 10
        if K_NO < 17:
            return

        try:
            kline = self.ma_1m_table
        except:
            return
        # ma_1m_table has gap where latest val equals 0
        if kline.iloc[K_NO - 1, 3] == 0:
            return
        list = []
        for i in range(0, list_count):
            tmp = 0
            for j in range(0, ma_length):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            val = tmp / ma_length
            val = round(val, 2)
            list.append(val)

        self.ma3_list = list
        return

    def cal_MA5_list(self):
        K_NO = self.k_num
        ma_length = 5
        list_count = 10
        if K_NO < 17:
            return

        try:
            kline = self.ma_1m_table
        except:
            return
        # ma_1m_table has gap where latest val equals 0
        if kline.iloc[K_NO - 1, 3] == 0:
            return
        list = []
        for i in range(0, list_count):
            tmp = 0
            for j in range(0, ma_length):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            val = tmp / ma_length
            val = round(val, 2)
            list.append(val)

        list_reverse = []
        for i in range(list_count, 0, -1):
            list_reverse.append(list[i - 1])

        self.ma5_list = list
        self.ma5_list_reverse = list_reverse
        #print(list)
        #print(list_reverse)
        return

    def cal_ma_60m(self):
        try:
            kline = self.ma_60m_table
        except:
            return

        # MA10
        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[10 - 1 - i, 3]
        self.MA10h_now = tmp/10
        self.MA10h_now = round(self.MA10h_now, 2)

    def get_MA10h_now(self):
        return self.MA10h_now

    def cal_1mk(self, bar_cnt):
        K_NO = self.k_num
        list_count = bar_cnt
        if K_NO < 56:
            return

        try:
            kline = self.ma_1m_table
        except:
            return

        if kline.iloc[K_NO - 1, 3] == 0:
            return

        ma_length = 5
        list_ma5 = []
        for i in range(0, list_count):
            tmp = 0
            for j in range(0, ma_length):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            val = tmp / ma_length
            val = round(val, 2)
            list_ma5.append(val)

        ma_length = 10
        list_ma10 = []
        for i in range(0, list_count):
            tmp = 0
            for j in range(0, ma_length):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            val = tmp / ma_length
            val = round(val, 2)
            list_ma10.append(val)

        ma_length = 20
        list_ma20 = []
        for i in range(0, list_count):
            tmp = 0
            for j in range(0, ma_length):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            val = tmp / ma_length
            val = round(val, 2)
            list_ma20.append(val)

        list_close = []
        for i in range(0, list_count):
            val = kline.iloc[K_NO - 1 - i, 3]
            list_close.append(val)

        onemk = []
        for i in range(0, list_count):
            onemk.append([list_close[i], list_ma5[i], list_ma10[i], list_ma20[i]])
        self.onemk = onemk
        return

    def get_onemk(self):
        return self.onemk


    def cal_delta_ma(self):
        K_NO = self.k_num
        if K_NO < 56:
            return

        try:
            kline = self.ma_1m_table
        except:
            return

        self.deltaMA20_now = (kline.iloc[K_NO - 1, 3] - kline.iloc[K_NO - 21, 3])/20
        self.deltaMA20_now = round(self.deltaMA20_now, 2)
        self.deltaMA20_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 22, 3])/20
        self.deltaMA20_cur = round(self.deltaMA20_cur, 2)
        self.deltaMA20_ma3 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] - kline.iloc[K_NO - 22, 3] - kline.iloc[K_NO - 23, 3] - kline.iloc[K_NO - 24, 3])/60
        self.deltaMA20_ma3 = round(self.deltaMA20_ma3, 2)
        self.deltaMA20_ma5 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] + kline.iloc[K_NO - 5, 3] + kline.iloc[K_NO - 6, 3] - kline.iloc[K_NO - 22, 3] - kline.iloc[K_NO - 23, 3] - kline.iloc[K_NO - 24, 3] - kline.iloc[K_NO - 25, 3] - kline.iloc[K_NO - 26, 3]) / 100
        self.deltaMA20_ma5 = round(self.deltaMA20_ma5, 2)

        self.deltaMA10_now = (kline.iloc[K_NO - 1, 3] - kline.iloc[K_NO - 11, 3])/10
        self.deltaMA10_now = round(self.deltaMA10_now, 2)
        self.deltaMA10_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 12, 3])/10
        self.deltaMA10_cur = round(self.deltaMA10_cur, 2)
        self.deltaMA10_ma3 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] - kline.iloc[K_NO - 12, 3] - kline.iloc[K_NO - 13, 3] - kline.iloc[K_NO - 14, 3])/30
        self.deltaMA10_ma3 = round(self.deltaMA10_ma3, 2)
        self.deltaMA10_ma5 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] + kline.iloc[K_NO - 5, 3] + kline.iloc[K_NO - 6, 3] - kline.iloc[K_NO - 12, 3] - kline.iloc[K_NO - 13, 3] - kline.iloc[K_NO - 14, 3] - kline.iloc[K_NO - 15, 3] - kline.iloc[K_NO - 16, 3]) / 50
        self.deltaMA10_ma5 = round(self.deltaMA10_ma5, 2)

        self.deltaMA50_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 52, 3])/50
        self.deltaMA50_cur = round(self.deltaMA50_cur, 2)

        # MA5
        tmp = 0
        for i in range(0, 5):
            tmp += kline.iloc[K_NO - 1 - i, 3]
        self.MA5_now = tmp / 5
        self.MA5_now = round(self.MA5_now, 2)

        tmp = 0
        for i in range(0, 5):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA5_cur = tmp / 5
        self.MA5_cur = round(self.MA5_cur, 2)

        # MA10
        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[K_NO - 1 - i, 3]
        self.MA10_now = tmp/10
        self.MA10_now = round(self.MA10_now, 2)

        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA10_cur = tmp/10
        self.MA10_cur = round(self.MA10_cur, 2)

        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA10_3 = tmp/10
        self.MA10_3 = round(self.MA10_3, 2)

        # MA20
        tmp = 0
        for i in range(0, 20):
            tmp += kline.iloc[K_NO - 1 - i, 3]
        self.MA20_now = tmp/20
        self.MA20_now = round(self.MA20_now, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA20_cur = tmp/20
        self.MA20_cur = round(self.MA20_cur, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA20_3 = tmp/20
        self.MA20_3 = round(self.MA20_3, 2)

        # MA50
        tmp = 0
        for i in range(0, 50):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA50_cur = tmp/50
        self.MA50_cur = round(self.MA50_cur, 2)

        tmp = 0
        for i in range(0, 50):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA50_3 = tmp/50
        self.MA50_3 = round(self.MA50_3, 2)

        return

    def get_deltaMA50_cur(self):
        return self.deltaMA50_cur

    def get_deltaMA20_now(self):
        return self.deltaMA20_now

    def get_deltaMA20_cur(self):
        return self.deltaMA20_cur

    def get_deltaMA20_ma3(self):
        return self.deltaMA20_ma3

    def get_deltaMA20_ma5(self):
        return self.deltaMA20_ma5

    def get_deltaMA10_now(self):
        return self.deltaMA10_now

    def get_deltaMA10_cur(self):
        return self.deltaMA10_cur

    def get_deltaMA10_ma3(self):
        return self.deltaMA10_ma3

    def get_deltaMA10_ma5(self):
        return self.deltaMA10_ma5

    def get_MA5_List_reverse(self):
        return self.ma5_list_reverse
    
    def get_MA3_List(self):
        return self.ma3_list

    def get_MA5_now(self):
        return self.MA5_now

    def get_MA5_List(self):
        return self.ma5_list

    def get_MA10_now(self):
        return self.MA10_now

    def get_MA10_cur(self):
        return self.MA10_cur

    def get_MA10_3(self):
        return self.MA10_3

    def get_MA20_now(self):
        return self.MA20_now

    def get_MA20_cur(self):
        return self.MA20_cur

    def get_MA20_3(self):
        return self.MA20_3

    def get_MA50_cur(self):
        return self.MA50_cur

    def get_MA50_3(self):
        return self.MA50_3

    def get_bull_bid(self):
        return self.bull_bid

    def get_bull_ask(self):
        return self.bull_ask

    def get_bear_bid(self):
        return self.bear_bid

    def get_bear_ask(self):
        return self.bear_ask

    def get_bull_bid_seller(self):
        return self.bull_bid_seller

    def get_bull_ask_seller(self):
        return self.bull_ask_seller

    def get_bear_bid_seller(self):
        return self.bear_bid_seller

    def get_bear_ask_seller(self):
        return self.bear_ask_seller

    def store_kday(self):
        self.get_ma_1m(1000000)
        self.ma_1m_table.to_csv("C:\\dayk_" + "2017all" + ".csv", index=False)

    def run(self):
        self.ready = 0
        ret_status = RET_OK
        ret_data = ""
        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("QUOTE")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("K_1M")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("K_60M")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("ORDER_BOOK")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("TICKER")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        self.test = 1
        i = 180
        while(1):
            start = time.time()
            ret = self.get_cur_stock_quoto()
            if ret == RET_ERROR:
                continue

            self.get_rt_ticker()
            self.get_ma_1m(self.k_num)
            self.get_ma_60m()
            if self.test == 0:
                self.store_kday()
                self.test = 1
                continue

            self.cal_1mk(7)
            self.cal_delta_ma()
            self.cal_ma_60m()
            self.cal_MA5_list()
            self.cal_MA3_list()
            self.cal_vol_ma()
            self.ready = 1
            print("CUR D:", self.cur_stock_quoto_delta)
            print("VOL D:", self.cur_stock_quoto_volume_delta)
            end = time.time()
            dur = end - start
            if dur < 0:
                continue
            if self.refresh < dur:
                #print("quoto duration overtime")
                continue
            else:
                time.sleep(self.refresh - dur)
            #i -= 1
        self.ready = 0
        print("Quoto Dies")