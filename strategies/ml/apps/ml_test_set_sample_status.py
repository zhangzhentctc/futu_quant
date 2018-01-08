from strategies.ml.data_handler.sample_handler import *


def set_all_avail():
    samp.set_all_avail()
    print("Set All Samples Avail!")

def set_sample_avail(id):
    samp.set_sample_avail(id)
    print("Set Sample", str(id), "Avail!")

def set_sample_avail_only(id):
    samp.set_sample_avail_only(id)
    print("Set Only Sample", str(id), "Avail!")

if __name__ == "__main__":

    samp = sample_handler()
    samp.init_db()

    #set_all_avail()
    set_sample_avail_only(3)

