from strategies.ml.test.data_handler.sample_handler import *
from strategies.ml.test.comparer.sample_comparer import *

onemk = [
    [20000, 20001, 20002, 20003],
    [20004, 20005, 20006, 20007],
    [20020, 20001, 20002, 20003],
    [20000, 20001, 20002, 20003],
[20000, 20001, 20002, 20003],
[20002, 20001, 20002, 20003],
[20004, 20003, 20002, 20003],
]

if __name__ == "__main__":
    samp_h = sample_handler()
    samp_h.init_db()
    samp_h.import_samples_from_db()
    samp_h.translation_samples()

    #samp_c = sample_comparer(samp_h, onemk)
    #samp_c.norm_compare_data()
    #print(onemk)
    #print(samp_c.onemk)
    #ret = samp_c.process_k_distance()
    #print(ret)

    samp_c = sample_comparer(samp_h, onemk)
    ret = samp_c.process_compare()
    print(ret)



