from openft.open_quant_context import *
import time
from data_src.ma.GetMovingAverage import *
from data_src.stock_info.get_stock_quote import *
from ui.TrendToast import *
from init import *
from db.store_control import *
from trade_api.hk_trade_api import *
from trade_api.hk_trade_op import *
from data_src.stock_info.stock_info import *
from strategies.zma.daytest import *
from strategies.zma.zma20_strategy_quote import *
from ui.PlaySound import *
from trade_api.hk_trader_placer import *
from db.store_ch_rate import *

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


if __name__ == "__main__":
#    test = daytest()
#    test.daytest()

    print("111111111111111111111")
    init = Initialize('127.0.0.1', 11111)
    quote_context = init.initialize()
    play = PlaySound()
    play.start()
    zma_str = zma20_strategy_quote(quote_context, play)
    zma_str.start()
    store_ch_rate = store_ch_rate(zma_str)
    store_ch_rate.start()
    while(1):
        ret, data = zma_str.get_cur_zma_quote()
        if ret == RET_OK:
            print("")
#            print(str(data["time"][0]) + "Attack: zma10_r_r:" + str(data["zma10_ratio_ratio"][0]) + " cur_r: " + str(data["cur_ratio"][0]))
#            print("         Defend: zma20_r:" + str(data["zma20_ratio"][0]) + " zma20_r_r " + str(data["zma20_ratio_ratio"][0]))
        time.sleep(0.5)

#    ma = MovingAverage(quote_context)
#    ma.start()

#    detectMATrend = DetectMATrend(quote_context, ma)
#    detectMATrend.start()
#    detectMATrend5 = DetectMATrend(quote_context, ma, 5)
#    detectMATrend5.start()

#    sc = store_control(detectMATrend, detectMATrend5, ma)
 #   sc.start()

 #   hk_trade = hk_trade_api()
#   hk_trade.initialize()
#    hk_trade.unlock_trade('88888888', '584679')
#    opt = hk_trade_opt(hk_trade)
 #   placer_c = hk_trader_placer(ma, opt, "C")
#    placer_p = hk_trader_placer(ma, opt, "P")


#    placer.buy()
#    localid = opt.buy(0.06, 10000, "67541")
#    orderid = opt.get_order_id(localid)
 #   status = opt.check_order_status(orderid)
#    dealt = opt.get_dealt_qty(orderid)
#    print(dealt)
#    opt.disable_order(orderid)

 #   trendToast = TrendToast(detectMATrend,detectMATrend5, placer_c, placer_p)
 #   trendToast.display()






#    while 1:
#        if detectSignal.detect() == 1:
#            print("Signal Trigger")
#        time.sleep(0.5)





 #   dayReview = DayReview(quote_context)
 #   dayReview.review()

#    _example_stock_quote(quote_context)
#    _example_cur_kline(quote_context)
#    _example_rt_ticker(quote_context)
#    _example_order_book(quote_context)
#    _example_get_trade_days(quote_context)
#    _example_stock_basic(quote_context)

#    quote_context.subscribe('HK.00700', "QUOTE", push=True)
