from strategies.ml.data_handler.sample_handler import *


if __name__ == "__main__":
    day = 20171013
    num = 1458
    sample_vals = [
[69, 73.2, 71.8, 71.05],
[76, 72.6, 72.4, 71.35],
[77, 72.4, 73.3, 71.6],
[78, 74, 74.2, 71.95],
[84, 76.8, 75.7, 72.45],
[82, 79.4, 76.3, 72.8],
[84, 81, 76.8, 73.4]
]
    type = 3
    samp = sample_handler()
    samp.init_db()
    samp.input_sample_mannual(day,num,sample_vals, type)
    print("Sample Added")
