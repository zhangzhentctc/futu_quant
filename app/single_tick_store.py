from init.init import *
from app.db.store_ticker import *
from app.shared_mem.store_buffer import *
from app.stock_info.get_stock_quote import *


if __name__ == "__main__":
    init = Initialize('127.0.0.1', 11111)
    quote_context = init.initialize()
    ticker_buff = store_buffer()
    ticker_buff.initialize()
    quoter = get_stock_quote(quote_context, ticker_buff)
    quoter.start()
    time.sleep(0.2)
    storer = store_ticker(ticker_buff)
    storer.start()
