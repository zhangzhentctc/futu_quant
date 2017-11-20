import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from strategies.ml.ui.whatthefuck import *
import pandas as pd


class test_ret_viewer:
    def __init__(self, comparer):
        self.wtf1 = whatthefuck()
        self.wtf2 = whatthefuck()
        self.comparer = comparer

    def __init_frame(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_quo = self.f.add_subplot(211)
        self.plot_sap = self.f.add_subplot(212)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_button(self):
        Button(self.root, text='BigNext->', command=lambda: self.show_quote(1)).pack()
        Button(self.root, text='<-BigBack', command=lambda: self.show_quote(-1)).pack()
        Button(self.root, text='Next->', command=lambda: self.show_sample(1)).pack()
        Button(self.root, text='<-Back', command=lambda: self.show_sample(-1)).pack()

    def __init_text(self):
        mytext = Text(self.root, width=50, height=5)
        mytext.pack()
        self.__refresh_ret_text(mytext, self.wtf1)

    def __refresh_ret_text(self, text, wtf):
        string = wtf.string
        text.delete(1.0, 'end')
        text.insert('end', string)
        text.after(100, self.__refresh_ret_text, text, wtf)

    def init_viwer(self):
        self.__init_frame()
        self.__init_button()
        self.__init_text()

    def start_viewer(self):
        self.root.mainloop()

    def init_plots(self):
        pd_quo_data = self.__format_kbars2plot(self.comparer.quo_data)
        self.plot_quo.clear()
        self.plot_quo.plot(pd_quo_data)
        self.canvs.draw()

        pd_sap_data = self.__format_kbars2plot(self.comparer.sap_data)
        self.wtf1.string = str(self.comparer.distance)
        self.plot_sap.clear()
        self.plot_sap.plot(pd_sap_data)
        self.canvs.draw()


    ### Show Quote
    def show_quote(self, step):
        self.comparer.move_next_quo(step)
        self.wtf1.string = str(self.comparer.distance)
        pd_data = self.__format_kbars2plot(self.comparer.quo_data)
        self.plot_quo.clear()
        self.plot_quo.plot(pd_data)
        self.canvs.draw()

    ## Show Sample
    def show_sample(self, step):
        self.comparer.move_next_sap(step)
        self.wtf1.string = str(self.comparer.distance)
        pd_data = self.__format_kbars2plot(self.comparer.sap_data)
        self.plot_sap.clear()
        self.plot_sap.plot(pd_data)
        self.canvs.draw()

    def __format_kbars2plot(self, cp_data):
        data = []
        for i in range(0, 7):
            data.append({
                "1": cp_data[i][0], "2": cp_data[i][1], "3": cp_data[i][2], "4": cp_data[i][3]
            })
        pd_data = pd.DataFrame(data, columns=["1", "2", "3", "4"])
        return pd_data

    def prepare_viewer(self):
        self.init_viwer()
        self.init_plots()
        self.start_viewer()

