from openft.open_quant_context import *
import threading
import time


class stockSimpleInfo(threading.Thread):
    def __init__(self, qc , cycle = 0.2):
        super(stockSimpleInfo, self).__init__()
        self.__quote_ctx = qc
        self.refresh_cycle =cycle
        self.ask = 0
        self.bid = 0

    def get_ask_bid(self):
        stock_code_list = ["HK.65724"]

        # subscribe "ORDER_BOOK"
        for stk_code in stock_code_list:
            ret_status, ret_data = self.__quote_ctx.subscribe(stk_code, "ORDER_BOOK")
            if ret_status != RET_OK:
                print("%s %s: %s" % (stk_code, "ORDER_BOOK", ret_data))
                exit()

        for stk_code in stock_code_list:
            ret_status, ret_data = self.__quote_ctx.get_order_book(stk_code)
            if ret_status == RET_ERROR:
                print(stk_code, ret_data)
                exit()
            print("%s ORDER_BOOK" % stk_code)
            print(ret_data)
            print("\n\n")
            print(ret_data["Ask"][0][0])
            print(ret_data["Bid"][0][0])
            self.ask = ret_data["Ask"][0][0]
            self.bid = ret_data["Bid"][0][0]

    def run(self):
        while(1):
            self.get_ask_bid()
            time.sleep(self.refresh_cycle)