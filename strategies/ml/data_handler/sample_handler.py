from db.db_ml import *
import pandas as pd

COL_SAMPLE_TYPE   = 30
COL_SAMPLE_STATUS = 31
COL_SAMPLE_ID     = 32
COL_SAMPLE_COMP_CNT= 33

class sample_handler:
    def __init__(self):
        self.length = -1

    def init_db(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "ml_k_analysis")
        self.db.connectMysql()
        self.dbop = db_ml()

    def import_samples_from_db(self):
        count = self.dbop.dbop_get_sample(self.db)
        if count == 0:
            print("Sample Data Does Not Exist")
            return -1
        data = []
        for i in range(0, count):
            line = self.dbop.dbop_get_sample_next(self.db)
            ## If status == 1
            if line[32] == 1:
                data.append({
                    "day": line[1], "num": line[2],
                    "k_end_1": line[ 3], "ma5_1": line[ 4], "ma10_1": line[ 5], "ma20_1": line[ 6],
                    "k_end_2": line[ 7], "ma5_2": line[ 8], "ma10_2": line[ 9], "ma20_2": line[10],
                    "k_end_3": line[11], "ma5_3": line[12], "ma10_3": line[13], "ma20_3": line[14],
                    "k_end_4": line[15], "ma5_4": line[16], "ma10_4": line[17], "ma20_4": line[18],
                    "k_end_5": line[19], "ma5_5": line[20], "ma10_5": line[21], "ma20_5": line[22],
                    "k_end_6": line[23], "ma5_6": line[24], "ma10_6": line[25], "ma20_6": line[26],
                    "k_end_7": line[27], "ma5_7": line[28], "ma10_7": line[29], "ma20_7": line[30],
                    "type":    line[31], "status":line[32], "id": line[0], "comp_cnt": line[33]
                })

        self.samples = pd.DataFrame(data, columns=[
                "day","num",
                "k_end_1", "ma5_1", "ma10_1", "ma20_1",
                "k_end_2", "ma5_2", "ma10_2", "ma20_2",
                "k_end_3", "ma5_3", "ma10_3", "ma20_3",
                "k_end_4", "ma5_4", "ma10_4", "ma20_4",
                "k_end_5", "ma5_5", "ma10_5", "ma20_5",
                "k_end_6", "ma5_6", "ma10_6", "ma20_6",
                "k_end_7", "ma5_7", "ma10_7", "ma20_7",
                "type", "status", "id", "comp_cnt"
        ])

        self.length = len(self.samples.index)
        return

    def get_sample_comp_cnt(self, sample_num):
        return self.samples.iloc[sample_num, COL_SAMPLE_COMP_CNT]

    def get_sample_status(self, sample_num):
        return self.samples.iloc[sample_num, COL_SAMPLE_STATUS]

    def get_sample_type(self, sample_num):
        return self.samples.iloc[sample_num, COL_SAMPLE_TYPE]

    def get_sample_id(self, sample_num):
        return self.samples.iloc[sample_num, COL_SAMPLE_ID]

    def prepare_samples(self):
        self.init_db()
        self.import_samples_from_db()


############### APP USE
    def __set_sample(self, day, num, sap_vals, type):
        self.dbop.dbop_insert_sample(self.db, day, num, sap_vals, type)

    def input_sample_mannual(self, day, num, sample_vals, type):
        self.__set_sample(day, num, sample_vals, type)
        return

    def set_all_avail(self):
        self.dbop.dbop_update_sample_status_all_enable(self.db)

    def set_sample_avail(self, id):
        self.dbop.dbop_update_sample_status(self.db, id, 1)

    def set_sample_avail_only(self, id):
        self.dbop.dbop_update_sample_status_all_disable(self.db)
        self.dbop.dbop_update_sample_status(self.db, id, 1)