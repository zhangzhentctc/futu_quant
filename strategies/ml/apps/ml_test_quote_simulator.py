from strategies.ml.comparer.sample_dayk_comparer import *
from strategies.ml.simulator.quote_simulator import *
import time


if __name__ == "__main__":
    date = 20171019
    q_simu = quote_simulator(date)
    q_simu.prepare_quote_simulator()
    while q_simu.get_next_data() == 0:
        print(q_simu.get_ret_data())
        time.sleep(2)
