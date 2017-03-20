from tkinter import *
from sample import *
from strategies.ma.detectSignal import *

class TrendToast:
    def __init__(self,quote_context):
        # Init tk
        self.qc = quote_context
        self.delay = 500
        self.top = Tk()
        self.text = Text(self.top)
        self.text.pack(expand=1, fill='both')

    def display(self):
        detectSignal = DetectSignal(self.qc)
        self.__show(self.text, detectSignal)
        self.top.mainloop()

    def __show(self,text,detectSignal):
        text.delete(1.0, 'end')
        ret = detectSignal.detect()
        if ret != 0:
            count = detectSignal.count
            if ret == 1:
                val = "Upward"
            else:
                val = "Downward"
            time = count*(self.delay/1000)
            val = val + " " + str(time)
        else:
            val = "Wait"

        text.insert('end', val)
        text.after(self.delay, self.__show, text, detectSignal)