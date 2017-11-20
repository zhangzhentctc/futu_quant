from strategies.ml.simulator.quote_simulator import *
from strategies.ml.simulator.sample_simulator import *

from strategies.ml.comparer.sample_comparer import *
from strategies.ml.ui.auto_viewer import *

def add_ui_ret(sub_ui_ret):
    for i in range (0, len(sub_ui_ret)):
        ui_ret.append(sub_ui_ret[i])


if __name__ == "__main__":
    date_list = ["20171019", "20171020", "20171115", "20171116", "20171117"]
    #date_list=[]
    ui_ret = []
    for date in date_list:
        q_simu = quote_simulator(date)
        q_simu.prepare_quote_simulator()

        s_simu = sample_simulator()
        s_simu.prepare_sample_simulator()

        comparer = sample_comparer(q_simu, s_simu)
        comparer.set_distance_t(40)
        comparer.init_compare_data()

        comparer.process_k_distance()
        add_ui_ret(comparer.ui_ret)

    print(ui_ret)

    if len(ui_ret) == 0:
        print("No Result!")
    else:
        viewer = auto_viewer(ui_ret, date_list)
        viewer.prepare_viewer()

