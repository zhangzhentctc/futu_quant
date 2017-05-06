from openft.open_quant_context import *

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

class Initialize:
    def __init__(self, host, async_port ):
        self.host = host
        self.async_port = async_port
    def initialize(self):
        quote_context = OpenQuoteContext(self.host, self.async_port)
        quote_context.set_handler(StockQuoteTest())
        quote_context.set_handler(OrderBookTest())
        quote_context.set_handler(CurKlineTest())
        quote_context.set_handler(TickerTest())
        quote_context.start()
        return quote_context