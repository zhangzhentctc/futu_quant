from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt

class show_plots:
    def __init__(self):
        pass

    def init_data(self):
        data = []
        self.len = 10
        for i in range(0,self.len):
            data.append({"A":(i - 5)+10000, "B":(10-i - 5)+10000, "C":(i*2 - 5)+10000, "D":(i/3 - 5)+10000})
        self.df = DataFrame(data, columns=["A","B","C","D"])


    def init_plot(self, total_num):
        plt.figure("stock")
        self.total_num = total_num


    def prepare_plot(self, data_list, num):
        if num > self.total_num or num <= 0:
            print("Bad Sub Plot Num!")
            return -1
        s = str(self.total_num) + "1" + str(num)
        s_int = int(s)

        plt.subplot(s_int)
        plt.plot(data_list)
        return 0

    def add_annotate(self, x, y, num, words):
        if num > self.total_num or num <= 0:
            print("Bad Sub Plot Num!")
            return -1
        s = str(self.total_num) + "1" + str(num)
        s_int = int(s)

        plt.subplot(s_int)
        plt.annotate(
            words,
            xy=(x, y),
            xytext=(x, y + 5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
        )
        return 0

    def show_plot(self):
        plt.show()


if __name__ == "__main__":

    pdc = show_plots()
    pdc.init_data()
    pdc.init_plot(3)

    A = pdc.df["A"]
    B = pdc.df["B"]
    C = pdc.df["C"]
    D = pdc.df["D"]
    pdc.prepare_plot(C, 1)
    pdc.prepare_plot(B, 2)
    pdc.prepare_plot(C, 3)
    pdc.add_annotate(2, 2, 1, "Hello1")
    pdc.add_annotate(1, 2, 2, "Hello2")
    pdc.add_annotate(0, -1, 3, "Hello3")
    pdc.show_plot()