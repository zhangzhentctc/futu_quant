from strategies.ml.comparer.sample_comparer import *
from strategies.ml.data_handler.sample_handler import *
import time

onemk = [
    [20000, 20001, 20002, 20003],
    [20004, 20005, 20006, 20007],
    [20020, 20001, 20002, 20003],
    [20000, 20001, 20002, 20003],
    [20000, 20001, 20002, 20003],
    [20002, 20001, 20002, 20003],
    [20004, 20003, 20002, 20003]
]

if __name__ == "__main__":
    start = time.time()
    samp_h = sample_handler()
    samp_h.prepare_samples()

    #samp_c = sample_comparer(samp_h, onemk)
    #samp_c.norm_compare_data()
    #print(onemk)
    #print(samp_c.onemk)
    #ret = samp_c.process_k_distance()
    #print(ret)

    samp_c = sample_comparer(samp_h, onemk)
    ret = samp_c.process_compare()
    print(ret)
    end = time.time()
    print("Time:", end-start)


