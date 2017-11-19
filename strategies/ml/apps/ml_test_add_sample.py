from strategies.ml.data_handler.sample_handler import *


if __name__ == "__main__":
    day = 20171110
    num = -1
    sample_vals = [
        [47, 48.4, 51.8, 53.25],
        [57, 50.2, 52.2, 53.9],
        [48, 51.6, 51, 54.1],
        [53, 52.4, 50.7, 53.9],
        [60, 53, 50.9, 53.6],
        [77, 59, 53.7, 54, 6],
        [70, 61.6, 55.9, 55]
    ]
    samp = sample_handler()
    samp.init_db()
    samp.input_sample_mannual(day,num,sample_vals)
    print("Sample Added")
