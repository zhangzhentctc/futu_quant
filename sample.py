from openft.open_quant_context import *
import time

# Examples for use the python functions
#
def _example_stock_quote(quote_ctx):
    stock_code_list = ["HK.65724"]

    # subscribe "QUOTE"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "QUOTE")
        if ret_status != RET_OK:
            print("%s %s: %s" % (stk_code, "QUOTE", ret_data))
            exit()

    ret_status, ret_data = quote_ctx.query_subscription()

    if ret_status == RET_ERROR:
        print(ret_status)
        exit()

    print(ret_data)

    ret_status, ret_data = quote_ctx.get_stock_quote(stock_code_list)
    if ret_status == RET_ERROR:
        print(ret_data)
        exit()
    quote_table = ret_data

    print("QUOTE_TABLE")
    print(quote_table)


def _example_cur_kline(quote_ctx):
    # subscribe Kline
    stock_code_list = ["HK_FUTURE.999010"]
    sub_type_list = ["K_1M"]

    for code in stock_code_list:
        for sub_type in sub_type_list:
            ret_status, ret_data = quote_ctx.subscribe(code, sub_type)
            if ret_status != RET_OK:
                print("%s %s: %s" % (code, sub_type, ret_data))
                exit()

    ret_status, ret_data = quote_ctx.query_subscription()

    if ret_status == RET_ERROR:
        print(ret_data)
        exit()

    print(ret_data)

    for code in stock_code_list:
        for ktype in ["K_1M"]:
            ret_code, ret_data = quote_ctx.get_cur_kline(code, 5, ktype)
            if ret_code == RET_ERROR:
                print(code, ktype, ret_data)
                exit()
            kline_table = ret_data
            print("%s KLINE %s" % (code, ktype))
            print(kline_table)
            print("\n\n")
            print(kline_table[["close", "time_key"]])
            print(kline_table["close"][0])


def _example_rt_ticker(quote_ctx):
    stock_code_list = ["US.AAPL", "HK.00700", "SZ.000001", "SH.601318"]

    # subscribe "TICKER"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "TICKER")
        if ret_status != RET_OK:
            print("%s %s: %s" % (stk_code, "TICKER", ret_data))
            exit()

    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.get_rt_ticker(stk_code, 10)
        if ret_status == RET_ERROR:
            print(stk_code, ret_data)
            exit()
        print("%s TICKER" % stk_code)
        print(ret_data)
        print("\n\n")


def _example_order_book(quote_ctx):
    stock_code_list = ["HK.65724"]

    # subscribe "ORDER_BOOK"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "ORDER_BOOK")
        if ret_status != RET_OK:
            print("%s %s: %s" % (stk_code, "ORDER_BOOK", ret_data))
            exit()

    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.get_order_book(stk_code)
        if ret_status == RET_ERROR:
            print(stk_code, ret_data)
            exit()
        print("%s ORDER_BOOK" % stk_code)
        print(ret_data)
        print("\n\n")
        print(ret_data["Ask"][0][0])

def _example_get_trade_days(quote_ctx):
    ret_status, ret_data = quote_ctx.get_trading_days("US", "2017-01-01", "2017-01-18")
    if ret_status == RET_ERROR:
        print(ret_data)
        exit()
    print("TRADING DAYS")
    for x in ret_data:
        print(x)


def _example_stock_basic(quote_ctx):
    ret_status, ret_data = quote_ctx.get_stock_basicinfo("US", "STOCK")
    if ret_status == RET_ERROR:
        print(ret_data)
        exit()
    print("stock_basic")
    print(ret_data)


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super().on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("StockQuoteTest ", content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super().on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("OrderBookTest", content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super().on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("CurKlineTest", content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super().on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("TickerTest", content)
        return RET_OK, content

class MovingAverage:
    def __init__(self, qc):
        self.__quote_ctx = qc

    def get_ma_10m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        print(ret_data)

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + 9, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[9: 10 + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= 9:
                        tmp_sum = 0
                        for j in range(0, 10):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / 10
                    count = count + 1

                # abandon the first 9 numbers
                ma10_value_list = whole_value_list[9:9+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA10": ma10_value_list[i], "time_key": time_list[i]})
                ma_10m_table = pd.DataFrame(data, columns=["MA10", "time_key"])

                return ma_10m_table

    def get_ma_20m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        print(ret_data)

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + 19, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[19: 20 + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= 19:
                        tmp_sum = 0
                        for j in range(0, 20):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / 20
                    count = count + 1

                # abandon the first 9 numbers
                ma20_value_list = whole_value_list[19:19+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA20": ma20_value_list[i], "time_key": time_list[i]})
                ma_20m_table = pd.DataFrame(data, columns=["MA20", "time_key"])

                return ma_20m_table

    def get_ma_Xm(self, number, x):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        print(ret_data)

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + x-1, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[x-1: x + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= x-1:
                        tmp_sum = 0
                        for j in range(0, x):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / x
                    count = count + 1

                # abandon the first 9 numbers
                ma_value_list = whole_value_list[x-1:x-1+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA-x": ma_value_list[i], "time_key": time_list[i]})
                ma_x_table = pd.DataFrame(data, columns=["MA-x", "time_key"])

                return ma_x_table

class DayReview:
    def __init__(self, qc):
        self.__quote_ctx = qc

    def review(self):
        ma = MovingAverage(quote_context)
        ma10 = ma.get_ma_10m(765)
        ma20 = ma.get_ma_20m(765)
        ma50 = ma.get_ma_Xm(765, 50)
        # Condition 1 : Downward Trend
        #   1. Define T, around 10 mins
        #   2. During T,
        #        MA-10M[i] < MA-20M[i]
        #   3. During T
        #        delta
        t = 2
        ch_rate = 0.8
        print("**************************")
        count = 0

        i = 0
        i += 15
        while i < 765 - 420:
            flag = 1
            if ma10['MA10'][i] > ma20['MA20'][i]:
                for j in range(1, t):
                    flag = 1
                    # In case index is our of range
                    if i + j >= 765:
                        flag = 0
                        break
                    # Condition 1 MA Value Compare
                    if ma10['MA10'][i + j] <= ma20['MA20'][i + j]:
                        flag = 0
                        break
                    # Condition 2 MA Trend
                    if ma10['MA10'][i + j] - ma10['MA10'][i + j - 1] < 0 or ma20['MA20'][i + j] - ma20['MA20'][
                                        i + j - 1] < 0:
                        flag = 0
                        break
                # Condition 3 MA change rate
                if flag == 1:
                    ma10_ch_rate = (ma10['MA10'][i + t] - ma10['MA10'][i]) / t
                    ma20_ch_rate = (ma20['MA20'][i + t] - ma20['MA20'][i]) / t
                    if abs(ma20_ch_rate) < ch_rate:
                        flag = 0
                    else:
                        print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
                if j == t - 1 and flag == 1:
                    while 1:
                        if i + j >= 765:
                            break
                        if ma10['MA10'][i + j] <= ma20['MA20'][i + j]:
                            break
                        j += 1
                    print("SUCCESS!!! Upward ")
                    print(str(i) + " " + ma10['time_key'][i])
                    print("Duration:" + str(j))
                    count += 1
                    i += j

            if ma10['MA10'][i] < ma20['MA20'][i]:
                for j in range(1, t):
                    flag = 1
                    # In case index is our of range
                    if i + j >= 765:
                        flag = 0
                        break
                    # Condition 1 Value Compare
                    if ma10['MA10'][i + j] >= ma20['MA20'][i + j]:
                        flag = 0
                        break
                    # Condition 2 MA Trend
                    if ma10['MA10'][i + j] - ma10['MA10'][i + j - 1] > 0 or ma20['MA20'][i + j] - ma20['MA20'][
                                        i + j - 1] > 0:
                        flag = 0
                        break
                if flag == 1:
                    ma10_ch_rate = (ma10['MA10'][i + t] - ma10['MA10'][i]) / t
                    ma20_ch_rate = (ma20['MA20'][i + t] - ma20['MA20'][i]) / t
                    if abs(ma20_ch_rate) < ch_rate:
                        flag = 0
                    else:
                        print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
                if j == t - 1 and flag == 1:
                    while 1:
                        if i + j >= 765:
                            break
                        if ma10['MA10'][i + j] >= ma20['MA20'][i + j]:
                            break
                        j += 1
                    print("SUCCESS!!! Downward")
                    print(str(i) + " " + ma10['time_key'][i])
                    print("Duration:" + str(j))

                    count += 1
                    i += j

            i += 1

        print("Finished " + str(count))
        # Condition 2 : Upward Trend
        #   1. Define T, around 10 mins
        #   2. During T,
        #        MA-10M[i] > MA-20M[i]
        #   3. During T
        #        delta

class DetectSignal:
    def __init__(self, qc):
        self.__quote_ctx = qc

    def detect(self):
        t = 2
        ch_rate = 0.8
        flag = 1

        ma = MovingAverage(quote_context)
        ma10 = ma.get_ma_10m(t)
        ma20 = ma.get_ma_20m(t)

        # Check Upward Trend
        if ma10['MA10'][0] > ma20['MA20'][0]:
            for j in range(1, t):
                flag = 1
                # Condition 1 MA Value Compare
                if ma10['MA10'][j] <= ma20['MA20'][j]:
                    flag = 0
                    break
                # Condition 2 MA Trend
                if ma10['MA10'][j] - ma10['MA10'][j - 1] < 0 or ma20['MA20'][j] - ma20['MA20'][j - 1] < 0:
                    flag = 0
                    break
            # Condition 3 MA change rate
            if flag == 1:
                ma10_ch_rate = (ma10['MA10'][t] - ma10['MA10'][0]) / t
                ma20_ch_rate = (ma20['MA20'][t] - ma20['MA20'][0]) / t
                if abs(ma20_ch_rate) < ch_rate:
                    flag = 0
                else:
                    print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
            if j == t - 1 and flag == 1:
                print("SUCCESS!!! Upward " + ma10['time_key'][0])
                return 1

        # Check Downward Trend
        if ma10['MA10'][0] < ma20['MA20'][0]:
            for j in range(1, t):
                flag = 1
                # Condition 1 Value Compare
                if ma10['MA10'][j] >= ma20['MA20'][j]:
                    flag = 0
                    break
                # Condition 2 MA Trend
                if ma10['MA10'][j] - ma10['MA10'][j - 1] > 0 or ma20['MA20'][j] - ma20['MA20'][ j - 1] > 0:
                    flag = 0
                    break
            if flag == 1:
                ma10_ch_rate = (ma10['MA10'][t] - ma10['MA10'][0]) / t
                ma20_ch_rate = (ma20['MA20'][t] - ma20['MA20'][0]) / t
                if abs(ma20_ch_rate) < ch_rate:
                    flag = 0
                else:
                    print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
            if j == t - 1 and flag == 1:
                print("SUCCESS!!! Downward " + ma10['time_key'][0])
                return 1
        return 0

if __name__ == "__main__":

    quote_context = OpenQuoteContext(host='127.0.0.1', async_port=11111)
    quote_context.set_handler(StockQuoteTest())
    quote_context.set_handler(OrderBookTest())
    quote_context.set_handler(CurKlineTest())
    quote_context.set_handler(TickerTest())
    quote_context.start()

    detectSignal = DetectSignal(quote_context)
    while 1:
        if detectSignal.detect() == 1:
            print("Signal Trigger")
        else:
            print("Wait...")
        time.sleep(0.5)

    dayReview = DayReview(quote_context)
    dayReview.review()

#    _example_stock_quote(quote_context)
#    _example_cur_kline(quote_context)
#    _example_rt_ticker(quote_context)
#    _example_order_book(quote_context)
#    _example_get_trade_days(quote_context)
#    _example_stock_basic(quote_context)

#    quote_context.subscribe('HK.00700', "QUOTE", push=True)
