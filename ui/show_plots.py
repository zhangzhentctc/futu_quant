from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#from matplotlib import pyplot
import math


class show_plots:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.origin_lines =[]
        self.yMinMax = []

    def init_data(self):
        data = []
        self.len = 10
        for i in range(0,self.len):
            data.append({"A":(i - 5)+10000, "B":(10-i - 5)+10000, "C":(i*2 - 5)+10000, "D":(i/3 - 5)+10000})
        self.df = DataFrame(data, columns=["A","B","C","D"])


    def init_plot(self, total_num, name= "stock"):
        self.fig = plt.figure(name)
        self.total_num = total_num
        if total_num == 5:

            ax2 = plt.subplot(512)
            ymajorLocator_2 = MultipleLocator(1.5)           # 将y轴主刻度标签设置为0.5的倍数
            ymajorFormatter_2 = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
            yminorLocator_2 = MultipleLocator(1.5)           # 将此y轴次刻度标签设置为0.1的倍数
            ax2.yaxis.set_major_locator(ymajorLocator_2)
            ax2.yaxis.set_major_formatter(ymajorFormatter_2)
            ax2.yaxis.set_minor_locator(yminorLocator_2)
            ax2.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax2.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

            ax3 = plt.subplot(513)
            ymajorLocator_3 = MultipleLocator(0.005)
            #ymajorFormatter_3 = FormatStrFormatter('%1.1111f')
            yminorLocator_3 = MultipleLocator(0.005)
            ax3.yaxis.set_major_locator(ymajorLocator_3)
            #ax3.yaxis.set_major_formatter(ymajorFormatter_3)
            ax3.yaxis.set_minor_locator(yminorLocator_3)

            ax3.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax3.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

            ax4 = plt.subplot(514)
            ymajorLocator_4 = MultipleLocator(0.004)
            #ymajorFormatter_4 = FormatStrFormatter('%1.1111f')
            yminorLocator_4 = MultipleLocator(0.004)
            ax4.yaxis.set_major_locator(ymajorLocator_4)
            #ax4.yaxis.set_major_formatter(ymajorFormatter_4)
            ax4.yaxis.set_minor_locator(yminorLocator_4)
            ax4.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax4.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

            ax5 = plt.subplot(515)
            ymajorLocator_5 = MultipleLocator(5)
            #ymajorFormatter_4 = FormatStrFormatter('%1.1111f')
            yminorLocator_5 = MultipleLocator(5)
            ax5.yaxis.set_major_locator(ymajorLocator_5)
            #ax4.yaxis.set_major_formatter(ymajorFormatter_4)
            ax5.yaxis.set_minor_locator(yminorLocator_5)
            ax5.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax5.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

        if total_num == 4:

            ax2 = plt.subplot(412)
            ymajorLocator_2 = MultipleLocator(1.5)  # 将y轴主刻度标签设置为0.5的倍数
            ymajorFormatter_2 = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
            yminorLocator_2 = MultipleLocator(1.5)  # 将此y轴次刻度标签设置为0.1的倍数
            ax2.yaxis.set_major_locator(ymajorLocator_2)
            ax2.yaxis.set_major_formatter(ymajorFormatter_2)
            ax2.yaxis.set_minor_locator(yminorLocator_2)
            ax2.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax2.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

            ax3 = plt.subplot(413)
            ymajorLocator_3 = MultipleLocator(0.01)
            #ymajorFormatter_3 = FormatStrFormatter('%1.1111f')
            yminorLocator_3 = MultipleLocator(0.01)
            ax3.yaxis.set_major_locator(ymajorLocator_3)
            #ax3.yaxis.set_major_formatter(ymajorFormatter_3)
            ax3.yaxis.set_minor_locator(yminorLocator_3)

            ax3.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            ax3.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

            ax4 = plt.subplot(414)
            #ymajorLocator_4 = MultipleLocator(0.004)
            #yminorLocator_4 = MultipleLocator(0.004)
            #ax4.yaxis.set_major_locator(ymajorLocator_4)
            #ax4.yaxis.set_minor_locator(yminorLocator_4)
            #ax4.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            #ax4.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度
            ymajorLocator_4 = MultipleLocator(5)
            yminorLocator_4 = MultipleLocator(5)
            ax4.yaxis.set_major_locator(ymajorLocator_4)
            ax4.yaxis.set_minor_locator(yminorLocator_4)
            ax4.xaxis.grid(True, which='major')
            ax4.yaxis.grid(True, which='minor')


    def prepare_plot(self, data_list, num):
        if num > self.total_num or num <= 0:
            print("Bad Sub Plot Num!")
            return -1
        s = str(self.total_num) + "1" + str(num)
        s_int = int(s)

        plt.subplot(s_int)
        plt.plot(data_list)
        return 0

    def add_annotate(self, x, y, num, words, place = 50, color = "red"):
        if num > self.total_num or num <= 0:
            print("Bad Sub Plot Num!")
            return -1
        s = str(self.total_num) + "1" + str(num)
        s_int = int(s)

        plt.subplot(s_int)
        ano = plt.annotate(
            words,
            xy=(x, y),
            xytext=(x, y + place),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")
        )
        return ano

    def show_plot(self):
        for i in range(0, self.total_num):
            s = str(self.total_num) + "1" + str(i+1)
            s_int = int(s)
            ax =  plt.subplot(s_int)
            plt.subplot(s_int)
            self.origin_lines.append(len(ax.lines))

            ymin,ymax = plt.ylim()
            self.yMinMax.append([ymin,ymax])
        #print("Lines:", self.origin_lines)
        #print("Y:", self.yMinMax)
        self.add_env()
        plt.show()

    def close_plot_all(self):
        plt.close('all')


    def get_cur_words(self, position):
        return self.data_handler.get_cur_words(position)

    def onclick(self, event):
        for i in range(0, self.total_num):
            s = str(self.total_num) + "1" + str(i+1)
            s_int = int(s)
            ax =  plt.subplot(s_int)
            plt.subplot(s_int)
            try:
                ax.lines.remove(ax.lines[self.origin_lines[i]])
            except:
                x=1
            try:
                ax.plot([event.xdata, event.xdata], [self.yMinMax[i][0], self.yMinMax[i][1]], linestyle="--")
            except:
                x=1

        try:
            self.tmp_ano.remove()
        except:
            print("remove fail")
            x=1

        position = math.ceil(event.xdata)
        words = self.get_cur_words(position)

        s = str(self.total_num) + "1" + str(1)
        s_int = int(s)
        ax = plt.subplot(s_int)
        self.tmp_ano = self.add_annotate(position, self.yMinMax[0][1], 1, words)

        #print(ax.annotate, "aaa")

        plt.show()

    def add_env(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

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