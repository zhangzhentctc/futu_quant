from strategies.ml.data_handler.dayk_handler import *


if __name__ == "__main__":
    date = "20171121"
    dayk_h = dayk_handler()
    dayk_h.init_db()
    dayk_h.import_dayk2db(date)
