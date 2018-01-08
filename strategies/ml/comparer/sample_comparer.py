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
        self.comp_cnt = int(self.s_simu.get_sample_comp_cnt())
        print(self.comp_cnt)

        self.quo_data_t = self.__deep_copy(self.quo_data)
        self.sap_data_t = self.__deep_copy(self.sap_data)

        self.cal_distance()
        return RET_OK

    def __deep_copy(self, dataset):
        dataset_cy = []
        for i in range(0, len(dataset)):
            row = []
            for j in range(0, len(dataset[0])):
                row.append(dataset[i][j])
            dataset_cy.append(row)
        return dataset_cy


    def cal_distance(self):
        self.__norm_quo_data()
        self.__norm_sap_data()
        sum = 0
        #weigh = [0.6, 0.6, 0.8, 1, 1, 4, 4]
        weigh = [1, 1, 1, 1, 1, 1, 1]
        #weigh = [1, 1, 1, 1, 1, 1, 1]
        for kbar in range(7 - self.comp_cnt, 7):
            for t_line in range(0, 4):
                t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
                if t_line == 0:
                    sum += t * t * weigh[kbar] * 2
                else:
                    sum += t * t * weigh[kbar]
        distance = math.sqrt(sum)
        distance /= self.comp_cnt
        distance = round(distance, 2)
        self.distance = distance

        sum2 = 0
        # weigh = [0.6, 0.6, 0.8, 1, 1, 4, 4]
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        for kbar in range(7 - self.comp_cnt, 7):
            for t_line in range(0, 1):
                t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
                if t_line == 0:
                    sum2 += t * t * weigh2[kbar]
                else:
                    sum2 += t * t * weigh2[kbar]
        distance_close = math.sqrt(sum2)
        distance_close /= self.comp_cnt
        distance_close = round(distance_close, 2)
        self.distance_close = distance_close

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        for kbar in range(7 - self.comp_cnt, 7):
            for t_line in range(1, 2):
                t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
                if t_line == 0:
                    sum2 += t * t * weigh2[kbar]
                else:
                    sum2 += t * t * weigh2[kbar]
        distance_ma5 = math.sqrt(sum2)
        distance_ma5 /= self.comp_cnt
        distance_ma5 = round(distance_ma5, 2)
        self.distance_ma5 = distance_ma5

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        for kbar in range(7 - self.comp_cnt, 7):
            for t_line in range(2, 3):
                t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
                if t_line == 0:
                    sum2 += t * t * weigh2[kbar]
                else:
                    sum2 += t * t * weigh2[kbar]
        distance_ma10 = math.sqrt(sum2)
        distance_ma10 /= self.comp_cnt
        distance_ma10 = round(distance_ma10, 2)
        self.distance_ma10 = distance_ma10

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        for kbar in range(7 - self.comp_cnt, 7):
            for t_line in range(3, 4):
                t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
                if t_line == 0:
                    sum2 += t * t * weigh2[kbar]
                else:
                    sum2 += t * t * weigh2[kbar]
        distance_ma20 = math.sqrt(sum2)
        distance_ma20 /= self.comp_cnt
        distance_ma20 = round(distance_ma20, 2)
        self.distance_ma20 = distance_ma20

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 6
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar7 = math.sqrt(sum2)
        distance_bar7 = round(distance_bar7, 2)
        self.distance_bar7 = distance_bar7


        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 5
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar6 = math.sqrt(sum2)
        distance_bar6 = round(distance_bar6, 2)
        self.distance_bar6 = distance_bar6

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 4
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar5 = math.sqrt(sum2)
        distance_bar5 = round(distance_bar5, 2)
        self.distance_bar5 = distance_bar5

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 3
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar4 = math.sqrt(sum2)
        distance_bar4 /= self.comp_cnt
        distance_bar4 = round(distance_bar4, 2)
        self.distance_bar4 = distance_bar4

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 2
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar3 = math.sqrt(sum2)
        distance_bar3 = round(distance_bar3, 2)
        self.distance_bar3 = distance_bar3

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 1
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar2 = math.sqrt(sum2)
        distance_bar2 = round(distance_bar2, 2)
        self.distance_bar2 = distance_bar2

        sum2 = 0
        weigh2 = [1, 1, 1, 1, 1, 1, 1]
        kbar = 0
        for t_line in range(0, 4):
            t = self.quo_data_t[kbar][t_line] - self.sap_data_t[kbar][t_line]
            if t_line == 0:
                sum2 += t * t * weigh2[kbar]
            else:
                sum2 += t * t * weigh2[kbar]

        distance_bar1 = math.sqrt(sum2)
        distance_bar1 = round(distance_bar1, 2)
        self.distance_bar1 = distance_bar1

        return distance


    def __norm_quo_data(self):
        samp_type = self.__get_sample_type()
        if samp_type >= 0:

            min = self.__find_dataset_min(self.quo_data_t)
            self.__translation_dataset(self.quo_data_t, min)
        else:

            max = self.__find_dataset_max(self.quo_data_t)
            self.__mirror_dataset(self.quo_data_t, max)
            min = self.__find_dataset_min(self.quo_data_t)
            self.__translation_dataset(self.quo_data_t, min)

    def __norm_sap_data(self):
        samp_type = self.__get_sample_type()
        if samp_type >= 0:
            align_ma5 = self.quo_data_t[7 - self.comp_cnt][1]
            gap = self.sap_data_t[7 - self.comp_cnt][1] - align_ma5
            self.__translation_dataset(self.sap_data_t, gap)

            #min = self.__find_dataset_min(self.sap_data_t)
            #self.__translation_dataset(self.sap_data_t, min)

        else:

            max = self.__find_dataset_max(self.sap_data_t)
            self.__mirror_dataset(self.sap_data_t, max)
            min = self.__find_dataset_min(self.sap_data_t)
            self.__translation_dataset(self.sap_data_t, min)


    def __find_dataset_min(self, dataset):
        min = dataset[0][0]
        for i in range(7 - self.comp_cnt, 7):
            for j in range(0, 4):
                if dataset[i][j] < min:
                    min = dataset[i][j]
        return min

    def __find_dataset_max(self, dataset):
        max = dataset[0][0]
        for i in range(7 - self.comp_cnt, 7):
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
        self.quo_data_t = self.__deep_copy(self.quo_data)
        self.cal_distance()
        return RET_OK

    def move_next_sap(self, step):
        ret = self.s_simu.get_next_data(step)
        if ret != 0:
            return RET_ERR

        self.sap_data = self.s_simu.get_ret_data()
        self.comp_cnt = int(self.s_simu.get_sample_comp_cnt())
        print(self.comp_cnt)
        self.sap_data_t = self.__deep_copy(self.sap_data)
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

    def get_sample_type(self):
        samp_type = self.s_simu.get_sample_type()
        return samp_type

    def get_sample_id(self):
        samp_id = self.s_simu.get_sample_id()
        return samp_id

    def get_quote_point(self):
        quo_ptr = self.q_simu.get_point()
        return quo_ptr

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
                        ui_ret.append([self.q_simu.date, self.__get_quote_point(), sample_type, distance, sample_id, 0])
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

