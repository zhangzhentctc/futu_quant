import math


class sample_comparer:
    def __init__(self, sample_handler, onemk, inspect_bars = 7):
        self.sample_handler = sample_handler
        self.inspect_bars = inspect_bars

        ## Deep Copy Compare Data
        self.onemk=[]
        for i in range(0, len(onemk)):
            raw_tmp = []
            for j in range(0, len(onemk[0])):
                raw_tmp.append(onemk[i][j])
            self.onemk.append(raw_tmp)

        self.comp_ret = []


    def __find_compare_data_min(self):
        all_min = self.onemk[0][0]
        for bar_num in range (0, self.inspect_bars):
            for j in range(0, 4):
                if self.onemk[bar_num][j] < all_min:
                    all_min = self.onemk[bar_num][j]
        return all_min

    def __is_sample_avail(self, sample_num):
        ## Check Status
        if self.sample_handler.get_sample_status(sample_num) == 1:
            return 1
        else:
            return 1

    def __is_distance_close(self, distance):
        if distance < 30:
            return 1
        else:
            return 0

    def __cal_distance(self, sample_num):
        if sample_num > self.sample_handler.length - 1 or sample_num < 0:
            return
        length = self.inspect_bars
        sum = 0
        weigh = [0.6, 0.6, 0.8, 1, 1, 4, 4]
        for i in range(0, length):
            tmp = 0
            t = self.onemk[i][0] - self.sample_handler.samples.iloc[sample_num, i * 4 + 2]
            tmp += t * t * 2
            t = self.onemk[i][1] - self.sample_handler.samples.iloc[sample_num, i * 4 + 3]
            tmp += t * t
            t = self.onemk[i][2] - self.sample_handler.samples.iloc[sample_num, i * 4 + 4]
            tmp += t * t
            t = self.onemk[i][3] - self.sample_handler.samples.iloc[sample_num, i * 4 + 5]
            tmp += t * t
            tmp *= weigh[i]
            sum += tmp
        distance = math.sqrt(sum)
        return distance

    def __find_best_pattern(self):
        if len(self.comp_ret) == 0:
            return -1
        else:
            min_index = 0
            min_distance = self.comp_ret[0][2]
            for index in range (0, len(self.comp_ret)):
                if self.comp_ret[index][2] < min_distance:
                    min_index = index
                    min_distance = self.comp_ret[index][2]
            return min_index

    def norm_compare_data(self):
        all_min = self.__find_compare_data_min()
        for bar_num in range(0, self.inspect_bars):
            for j in range(0, 4):
                self.onemk[bar_num][j] -= all_min
        return

    def process_k_distance(self):
        comp_ret = []
        for sample_num in range(0, self.sample_handler.length):
            if self.__is_sample_avail(sample_num) == 1:
                distance = self.__cal_distance(sample_num)
                sample_type = self.sample_handler.get_sample_type(sample_num)
                sample_id = self.sample_handler.get_sample_id(sample_num)
                if self.__is_distance_close(distance) == 1:
                    comp_ret.append([sample_id, sample_type, distance])
        self.comp_ret = comp_ret
        return

    def get_best_pattern_info(self):
        min_index = self.__find_best_pattern()
        if min_index == -1:
            return 0
        else:
            return self.comp_ret[min_index][1]

    def process_compare(self):
        self.norm_compare_data()
        self.process_k_distance()
        ret = self.get_best_pattern_info()
        return ret

