import math


RET_OK = 0
RET_ERR = -1
class sample_comparer:
    def __init__(self, q_simu, s_simu):
        self.q_simu = q_simu
        self.s_simu = s_simu
        self.distance = -1
        self.distance_T = 30

    def init_compare_data(self):
        ret = self.q_simu.get_next_data(0)
        if ret != RET_OK:
            return RET_ERR

        ret = self.s_simu.get_next_data(0)
        if ret != RET_OK:
            return RET_ERR

        self.quo_data = self.q_simu.get_ret_data()
        self.sap_data = self.s_simu.get_ret_data()

        self.cal_distance()
        return RET_OK

    def cal_distance(self):
        self.__norm_quo_data()
        sum = 0
        weigh = [0.6, 0.6, 0.8, 1, 1, 4, 4]
        for i in range(0, 7):
            for j in range(0, 4):
                t = self.quo_data[i][j] - self.sap_data[i][j]
                if j == 0:
                    sum += t * t * weigh[i] * 2
                else:
                    sum += t * t * weigh[i]
        distance = math.sqrt(sum)
        self.distance = distance
        return distance


    def __norm_quo_data(self):
        samp_type = self.__get_sample_type()
        if samp_type >= 0:
            min = self.__find_dataset_min(self.quo_data)
            self.__translation_dataset(self.quo_data, min)
        else:
            max = self.__find_dataset_max(self.quo_data)
            self.__mirror_dataset(self.quo_data, max)
            min = self.__find_dataset_min(self.quo_data)
            self.__translation_dataset(self.quo_data, min)


    def __find_dataset_min(self, dataset):
        min = dataset[0][0]
        for i in range(0, 7):
            for j in range(0, 4):
                if dataset[i][j] < min:
                    min = dataset[i][j]
        return min

    def __find_dataset_max(self, dataset):
        max = dataset[0][0]
        for i in range(0, 7):
            for j in range(0, 4):
                if dataset[i][j] > max:
                    max = dataset[i][j]
        return max

    def __mirror_dataset(self, dataset, val):
        for i in range(0, 7):
            for j in range(0, 4):
                dataset[i][j] = 2 * val - dataset[i][j]
        return

    def __translation_dataset(self, dataset, val):
        for i in range(0, 7):
            for j in range(0, 4):
                dataset[i][j] = dataset[i][j] - val
        return

    def move_next_quo(self, step):
        ret = self.q_simu.get_next_data(step)
        if ret != 0:
            return RET_ERR

        self.quo_data = self.q_simu.get_ret_data()
        self.cal_distance()
        return RET_OK

    def move_next_sap(self, step):
        ret = self.s_simu.get_next_data(step)
        if ret != 0:
            return RET_ERR

        self.sap_data = self.s_simu.get_ret_data()
        self.cal_distance()
        return RET_OK

    def __is_sample_avail(self):
        if self.s_simu.get_sample_status() == 1:
            return RET_OK
        else:
            return RET_ERR

    def __is_distance_close(self):
        if self.distance < self.distance_T:
            return RET_OK
        else:
            return RET_ERR

    def __get_sample_type(self):
        samp_type = self.s_simu.get_sample_type()
        return samp_type

    def __get_sample_id(self):
        samp_id = self.s_simu.get_sample_id()
        return samp_id

    def __get_quote_point(self):
        quo_ptr = self.q_simu.get_point()
        return quo_ptr

    ## Compare Quote with all the samples
    def process_k_distance(self):
        comp_ret = []
        ui_ret = []
        while self.move_next_quo(1) == RET_OK:
            while self.move_next_sap(1) == RET_OK:
                if self.__is_sample_avail() == RET_OK:
                    distance = self.distance
                    sample_type = self.__get_sample_type()
                    sample_id = self.__get_sample_id()
                    if self.__is_distance_close() == RET_OK:
                        comp_ret.append([sample_id, sample_type, distance])
                        ui_ret.append([self.q_simu.date, self.__get_quote_point(), sample_type, distance, 0, 0])
            self.s_simu.reset_point()
        self.comp_ret = comp_ret
        self.ui_ret = ui_ret
        return

    def process_k_distance_single(self):
        comp_ret = []
        if self.__is_sample_avail() == RET_OK:
            distance = self.cal_distance()
            sample_type = self.__get_sample_type()
            sample_id = self.__get_sample_id()
            if self.__is_distance_close() == RET_OK:
                comp_ret.append([sample_id, sample_type, distance])
        self.comp_ret = comp_ret
        return

    def __find_best_pattern(self):
        if len(self.comp_ret) == 0:
            return RET_ERR
        else:
            min_index = 0
            min_distance = self.comp_ret[0][2]
            for index in range (0, len(self.comp_ret)):
                if self.comp_ret[index][2] < min_distance:
                    min_index = index
                    min_distance = self.comp_ret[index][2]
            return min_index


    def get_best_pattern_info(self):
        min_index = self.__find_best_pattern()
        if min_index == -1:
            return RET_OK
        else:
            self.best_retset = self.comp_ret[min_index]
            return self.comp_ret[min_index][1]

    ### Total
    def process_compare(self):
        self.process_k_distance()
        ret = self.get_best_pattern_info()
        return ret

    def process_compare_single(self, sample_num):
        self.process_k_distance_single()
        ret = self.get_best_pattern_info()
        return ret

    def set_distance_t(self, distance):
        self.distance_T = distance

