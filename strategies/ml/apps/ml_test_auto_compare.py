from strategies.ml.simulator.quote_simulator import *
from strategies.ml.simulator.sample_simulator import *

from strategies.ml.comparer.sample_comparer import *
from strategies.ml.ui.auto_viewer import *

def add_ui_ret(sub_ui_ret):
    for i in range (0, len(sub_ui_ret)):
        ui_ret.append(sub_ui_ret[i])


class auto_operator:
    def __init__(self, sample_comparer):
        self.samp_comp = sample_comparer
        self.ui_ret = []

    def operate(self):
        while(1):
            distance = self.samp_comp.distance
            if distance <= self.samp_comp.distance_T and self.samp_comp.distance_ma5 < 0.5:
                self.ui_ret.append([self.samp_comp.q_simu.date,
                                    self.samp_comp.get_quote_point(),
                                    self.samp_comp.get_sample_type(),
                                    distance,
                                    self.samp_comp.get_sample_id(),
                                    #5
                                    self.samp_comp.distance_close,
                                    self.samp_comp.distance_ma5,
                                    self.samp_comp.distance_ma10,
                                    self.samp_comp.distance_ma20,
                                    #9
                                    self.samp_comp.distance_bar7,
                                    self.samp_comp.distance_bar6,
                                    self.samp_comp.distance_bar5,
                                    self.samp_comp.distance_bar4,
                                    self.samp_comp.distance_bar3,
                                    self.samp_comp.distance_bar2,
                                    self.samp_comp.distance_bar1
                                    ])

            if self.samp_comp.move_next_sap(1) == RET_ERR:
                if self.samp_comp.move_next_quo(1) == RET_ERR:
                    break
                self.samp_comp.s_simu.reset_point()





if __name__ == "__main__":
    date_list = ["20171019", "20171020", "20171115", "20171116", "20171117", "20171120", "20171121"]
    #date_list=[]
    ui_ret = []
    for date in date_list:
        q_simu = quote_simulator(date)
        q_simu.prepare_quote_simulator()

        s_simu = sample_simulator()
        s_simu.prepare_sample_simulator()

        comparer = sample_comparer(q_simu, s_simu)
        comparer.set_distance_t(6)
        comparer.init_compare_data()
        op = auto_operator(comparer)
        op.operate()

        add_ui_ret(op.ui_ret)

    print(ui_ret)
    date_list_all = ["20171019", "20171020", "20171115", "20171116", "20171117", "20171120", "20171121"]
    if len(ui_ret) == 0:
        print("No Result!")
    else:
        viewer = auto_viewer(ui_ret, date_list_all)
        viewer.prepare_viewer()

