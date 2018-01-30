from tkinter import *
from app.db.ticker_handler import *

DEF_WIDTH_CHARS = 100
DEF_HIGHT_CHARS =  30
DEF_FONT = 10

MAX_WIDTH = DEF_WIDTH_CHARS * DEF_FONT
MAX_HIGHT = DEF_HIGHT_CHARS * DEF_FONT

BUY_CYB = '+'
SELL_CYB = '#'
NEUL_CYB = '='
ZOOM = 1/2

class viewer:
    def __init__(self, ticker_h):
        self.ticker_h = ticker_h
        self.root = Tk()


    def __init_bars(self):
        self.text_diagram = Text(self.root, width=DEF_WIDTH_CHARS, height=DEF_HIGHT_CHARS, font =("OCR-B", DEF_FONT, "normal"))

        self.text_diagram.config(state=DISABLED)

        bar = Scrollbar(self.root)
        bar.config(command=self.text_diagram.yview)
        self.text_diagram.config(yscrollcommand=bar.set)
        bar.pack(side=RIGHT,fill=Y)
        self.text_diagram.pack(side=LEFT,fill=BOTH,expand=1)


    def draw_bars(self):
        dig_str = ""
        dig_str += "From:" + self.start_time + " To:" + self.end_time + '\n'
        for i in range(len(self.data_prices_l) - 1, -1, -1):
            dig_str += str(self.data_prices_l[i]) + " | "
            for cnt in range(0, int(self.data_buy_l[i]*ZOOM)):
                dig_str += BUY_CYB
            for cnt in range(0, int(self.data_sell_l[i]*ZOOM)):
                dig_str += SELL_CYB
            for cnt in range(0, int(self.data_neul_l[i]*ZOOM)):
                dig_str += NEUL_CYB
            dig_str += '\n'
        self.text_diagram.config(state=NORMAL)
        self.text_diagram.insert('insert', dig_str)
        self.text_diagram.config(state=DISABLED)



    def __init_controller(self):
        Button(self.root, text='10s  ->', command=lambda: self.__refresh_bars(10)).pack()
        Button(self.root, text='10s  <-', command=lambda: self.__refresh_bars(-10)).pack()
        Button(self.root, text='1Min ->>', command=lambda: self.__refresh_bars(60)).pack()
        Button(self.root, text='1Min <<-', command=lambda: self.__refresh_bars(-60)).pack()
        self.btn_starter = Button(self.root, text='Input Start Time', command=self.__get_start_time).pack()
        self.eny_starter = Entry(self.root, show=None)
        self.eny_starter.pack()
        Button(self.root, text='reset', command=lambda: self.__refresh_bars(-60)).pack()

    def __get_start_time(self):
        self.start_time = self.eny_starter.get()
        self.ticker_h.set_start(self.start_time)


    def init_viewer(self):
        self.__init_bars()
        self.__init_controller()

    def start_viewer(self):
        self.__refresh_bars(60)
        #self.canvs.draw()
        self.root.mainloop()


    def __refresh_bars(self, step):
        self.__get_next_bar_data(step)
        self.draw_bars()

    def __get_next_bar_data(self, step):
        self.ticker_h.move_end_ptr(step)
        self.ticker_h.gen_data()

        self.data_prices_l = self.ticker_h.price_l
        self.data_buy_l = self.ticker_h.buy_l
        self.data_neul_l = self.ticker_h.neul_l
        self.data_sell_l = self.ticker_h.sell_l
        self.start_time = self.ticker_h.get_start_time()
        self.end_time = self.ticker_h.get_end_time()


ticker_h = ticker_handler()
ticker_h.init_db()
ticker_h.import_tickers_from_db()

v = viewer(ticker_h)
v.init_viewer()
#v.set_auto_refresh()
v.start_viewer()
