import matplotlib
from strategies.ml.comparer.sample_dayk_comparer import *
from strategies.ml.data_handler.dayk_handler import *
from strategies.ml.data_handler.sample_handler import *
from strategies.ml.comparer.sample_dayk_comparer import *
from strategies.ml.simulator.quote_simulator import *
from strategies.ml.simulator.sample_simulator import *
from strategies.ml.comparer.inter_comparer import *
#from strategies.ml.comparer.sample_comparer import *
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *


class whatthefuck:
    def __init__(self):
        self.cnt = 0
        self.string = ""

    def add_x(self, x):
        self.cnt += x

    def assign(self, val):
        self.cnt = val

class sample_comparer:
    def __init__(self, q_simu, s_simu):
        self.q_simu = q_simu
        self.s_simu = s_simu
        self.distance = -1



class test_ret_viewer:
    def __init__(self, simulator, s_simu):
        self.wtf1 = whatthefuck()
        self.wtf2 = whatthefuck()
        self.simulator = simulator
        self.s_simu = s_simu
        self.distance = -1

    def __init_frame(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_quo = self.f.add_subplot(211)
        self.plot_sap = self.f.add_subplot(212)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_button(self):
        Button(self.root, text='BigNext->', command=lambda: self.show_result( 1)).pack()
        Button(self.root, text='<-BigBack', command=lambda: self.show_result(-1)).pack()
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

    def init_compare_data(self):
        ret = self.simulator.get_next_data(0)
        if ret != 0:
            return

        ret = self.s_simu.get_next_data(0)
        if ret != 0:
            return

        self.quo_data = self.simulator.get_ret_data()
        self.sap_data = self.s_simu.get_ret_data()

        self.cal_distance()

        pd_quo_data = self.__format_kbars2plot(self.quo_data)
        self.plot_quo.clear()
        self.plot_quo.plot(pd_quo_data)
        self.canvs.draw()

        pd_sap_data = self.__format_kbars2plot(self.sap_data)
        self.plot_sap.clear()
        self.plot_sap.plot(pd_sap_data)
        self.canvs.draw()


    ### Show Quote
    def show_result(self, step):
        ret = self.simulator.get_next_data(step)
        if ret != 0:
            return

        self.quo_data = self.simulator.get_ret_data()
        self.cal_distance()
        pd_data = self.__format_kbars2plot(self.quo_data)
        self.plot_quo.clear()
        self.plot_quo.plot(pd_data)
        self.canvs.draw()


    ## Show Sample
    def show_sample(self, step):
        ret = self.s_simu.get_next_data(step)
        if ret != 0:
            return

        self.sap_data = self.s_simu.get_ret_data()
        self.cal_distance()
        pd_data = self.__format_kbars2plot(self.sap_data)
        self.plot_sap.clear()
        self.plot_sap.plot(pd_data)
        self.canvs.draw()

    def cal_distance(self):
        self.norm_quo_data()
        sum = 0
        weigh = [0.6, 0.6, 0.8, 1, 1, 4, 4]
        for i in range(0, 7):
            for j in range(0, 4):
                t = self.quo_data[i][j] - self.sap_data[i][j]
                if j == 0:
                    sum += t * t * weigh[i] * 2
                else:
                    sum += t * t * weigh[i]
        distance = math.sqrt(sum)
        self.wtf1.string = str(distance)
        self.distance = distance
        print(distance)


    def norm_quo_data(self):
        samp_type = self.s_simu.get_sample_type()
        if samp_type >= 0:
            min = self.__find_dataset_min(self.quo_data)
            self.__translation_dataset(self.quo_data, min)
        else:
            max = self.__find_dataset_max(self.quo_data)
            self.__mirror_dataset(self.quo_data, max)
            min = self.__find_dataset_min(self.quo_data)
            self.__translation_dataset(self.quo_data, min)


    def __find_dataset_min(self, dataset):
        min = dataset[0][0]
        for i in range(0, 7):
            for j in range(0, 4):
                if dataset[i][j] < min:
                    min = dataset[i][j]
        return min

    def __find_dataset_max(self, dataset):
        max = dataset[0][0]
        for i in range(0, 7):
            for j in range(0, 4):
                if dataset[i][j] > max:
                    max = dataset[i][j]
        return max

    def __mirror_dataset(self, dataset, val):
        for i in range(0, 7):
            for j in range(0, 4):
                dataset[i][j] = 2 * val - dataset[i][j]
        return

    def __translation_dataset(self, dataset, val):
        for i in range(0, 7):
            for j in range(0, 4):
                dataset[i][j] = dataset[i][j] - val
        return


    def __format_kbars2plot(self, cp_data):
        data = []
        for i in range(0, 7):
            # self.f_plot.plot([cp_data[i][0], cp_data[i][1], cp_data[i][2], cp_data[i][3]])

            data.append({
                "1": cp_data[i][0], "2": cp_data[i][1], "3": cp_data[i][2], "4": cp_data[i][3]
            })
            #print(cp_data[i][0], " ", cp_data[i][1], " ", cp_data[i][2], " ", cp_data[i][3])
        pd_data = pd.DataFrame(data, columns=["1", "2", "3", "4"])
        return pd_data




if __name__ == "__main__":
    date_list = ["20171019", "20171020", "20171115", "20171116", "20171117"]

    q_simu = quote_simulator("20171019")
    q_simu.prepare_quote_simulator()

    samp_h = sample_handler()
    samp_h.prepare_samples()
    s_simu = sample_simulator(samp_h)

    viewer = test_ret_viewer(q_simu, s_simu)

    viewer.init_viwer()
    viewer.init_compare_data()
    viewer.start_viewer()