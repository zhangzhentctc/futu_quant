from db.db_ml import *
import pandas as pd


class sample_handler:
    def __init__(self):
        self.length = -1

    def init_db(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "ml_k_analysis")
        self.db.connectMysql()
        self.dbop = db_ml()

    def set_sample(self, day, num, sap_vals):
        self.dbop.dbop_insert_sample(self.db, day, num, sap_vals)

    def input_sample_mannual(self, day, num, sample_vals):
        self.set_sample(day, num, sample_vals)
        return


    def remove_sample_day(self, day):
        pass


    def import_samples_from_db(self):
        count = self.dbop.dbop_get_sample(self.db)
        if count == 0:
            print("Sample Data Does Not Exist")
            return -1
        data = []
        for i in range(0, count):
            line = self.dbop.dbop_get_sample_next(self.db)
            data.append({
                "day": line[1], "num": line[2],
                "k_end_1": line[ 3], "ma5_1": line[ 4], "ma10_1": line[ 5], "ma20_1": line[ 6],
                "k_end_2": line[ 7], "ma5_2": line[ 8], "ma10_2": line[ 9], "ma20_2": line[10],
                "k_end_3": line[11], "ma5_3": line[12], "ma10_3": line[13], "ma20_3": line[14],
                "k_end_4": line[15], "ma5_4": line[16], "ma10_4": line[17], "ma20_4": line[18],
                "k_end_5": line[19], "ma5_5": line[20], "ma10_5": line[21], "ma20_5": line[22],
                "k_end_6": line[23], "ma5_6": line[24], "ma10_6": line[25], "ma20_6": line[26],
                "k_end_7": line[27], "ma5_7": line[28], "ma10_7": line[29], "ma20_7": line[30]
            })

        self.samples = pd.DataFrame(data, columns=[
                "day","num",
                "k_end_1", "ma5_1", "ma10_1", "ma20_1",
                "k_end_2", "ma5_2", "ma10_2", "ma20_2",
                "k_end_3", "ma5_3", "ma10_3", "ma20_3",
                "k_end_4", "ma5_4", "ma10_4", "ma20_4",
                "k_end_5", "ma5_5", "ma10_5", "ma20_5",
                "k_end_6", "ma5_6", "ma10_6", "ma20_6",
                "k_end_7", "ma5_7", "ma10_7", "ma20_7"
        ])

        self.length = len(self.samples.index)
        return


    def translation_samples(self):
        for i in range(0, self.length):
            row_min = self.samples.iloc[i, 2]
            for j in range(3, 30):
                if self.samples.iloc[i, j] < row_min:
                    row_min = self.samples.iloc[i, j]
            for j in range(2, 30):
                self.samples.iloc[i, j] -= row_min
        return

