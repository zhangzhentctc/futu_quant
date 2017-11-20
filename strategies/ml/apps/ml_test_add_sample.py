from strategies.ml.data_handler.sample_handler import *


if __name__ == "__main__":
    day = 20171108
    num = -1
    sample_vals = [
        [123, 131.4, 137.9, 146.6],
        [123, 129.2, 134, 145.45],
        [108, 125.2, 129.5, 143.5],
        [114, 120.6, 126.7, 141.2],
        [116, 116.8, 124.7, 139.4],
        [112, 114.6, 123, 136.85],
        [96, 109.2, 119.2, 133.35],
    ]
    type = -2
    samp = sample_handler()
    samp.init_db()
    samp.input_sample_mannual(day,num,sample_vals, type)
    print("Sample Added")
