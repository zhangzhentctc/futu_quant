from strategies.ml.simulator.quote_simulator import *
from strategies.ml.simulator.sample_simulator import *

from strategies.ml.comparer.sample_comparer import *

from strategies.ml.ui.manual_viewer import *

if __name__ == "__main__":
    date_list = ["20171019", "20171020", "20171115", "20171116", "20171117"]

    q_simu = quote_simulator("20171019")
    q_simu.prepare_quote_simulator()


    s_simu = sample_simulator()
    s_simu.prepare_sample_simulator()

    comparer = sample_comparer(q_simu, s_simu)
    comparer.set_distance_t(50)
    comparer.init_compare_data()

    #comparer.process_k_distance()
    #print(comparer.ui_ret)

    viewer = test_ret_viewer(comparer)
    viewer.prepare_viewer()
