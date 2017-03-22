from data_src.ma.GetMovingAverage import *
import threading
import time

#
# Following Members are for construction
#    1. __quote_ctx: Context
#    2. duration:    Sample Period for judge      Default:2 s
#    3. interval:    Cycle time to refresh trend  Default:500 ms
#    4. ch_rate:     minimun Change Rate for MA
# Following Menmbers are to store data
#    1. count
#    2. trend
#    3. ma10_ch_rate
#    4. ma20_ch_rate
class DetectMATrend(threading.Thread):
    def __init__(self, qc, ma, duration = 2, interval = 500, ch_rate = 0.8):
        super(DetectMATrend, self).__init__()
        self.ma = ma
        self.__quote_ctx = qc
        self.duration = duration
        self.interval = interval
        self.ch_rate = ch_rate

        self.count = 0
        self.trend = 0
        self.ma10_ch_rate = 0
        self.ma20_ch_rate = 0

#
# Detect Current Trend
# Condition (During an interval t):
#     1. MA10 and MA20 have the same direction
#     2. MA10 and MA20 have no cross
#     3. MA10 and MA20 have a standard change rate
# Para:
#     t: Interval
#     ch_rate: standard change rate, delta value / interval
# Return:
#     0 stands no trend
#     1 stands upward trend
#    -1 stands downward trend

    def detect(self):
        flag = 1

        ma10 = self.ma.get_get_ma_10m_data(self.duration)
        ma20 = self.ma.get_get_ma_20m_data(self.duration)
        if len(ma10) == 0 or len(ma20) == 0:
            return 0

        self.ma10_ch_rate = (ma10['MA10'][self.duration - 1] - ma10['MA10'][0]) / self.duration
        self.ma20_ch_rate = (ma20['MA20'][self.duration - 1] - ma20['MA20'][0]) / self.duration
        # Check Upward Trend
        if ma10['MA10'][0] > ma20['MA20'][0]:
            for j in range(1, self.duration):
                flag = 1
                # Condition 1 MA Value Compare
                if ma10['MA10'][j] <= ma20['MA20'][j]:
                    flag = 0
                    self.count = 0
                    break
                # Condition 2 MA Trend
                if ma10['MA10'][j] - ma10['MA10'][j - 1] < 0 or ma20['MA20'][j] - ma20['MA20'][j - 1] < 0:
                    flag = 0
                    self.count = 0
                    break

            # Condition 3 MA Change Rate Filter
            if flag == 1:
                if abs(self.ma20_ch_rate) < self.ch_rate or abs(self.ma10_ch_rate) < self.ch_rate :
                    flag = 0
                    self.count = 0
                else:
                    print("\nM10 Ch:" + str(self.ma10_ch_rate) + "  " + "M20 Ch:" + str(self.ma20_ch_rate))
            if j == self.duration - 1 and flag == 1:
                print("SUCCESS!!! Upward " + ma10['time_key'][0] + " " + str(self.count))
                self.count += 1
                return 1

        # Check Downward Trend
        if ma10['MA10'][0] < ma20['MA20'][0]:
            for j in range(1, self.duration):
                flag = 1
                # Condition 1 Value Compare
                if ma10['MA10'][j] >= ma20['MA20'][j]:
                    flag = 0
                    self.count = 0
                    break
                # Condition 2 MA Trend
                if ma10['MA10'][j] - ma10['MA10'][j - 1] > 0 or ma20['MA20'][j] - ma20['MA20'][ j - 1] > 0:
                    flag = 0
                    self.count = 0
                    break
            if flag == 1:
                if abs(self.ma20_ch_rate) < self.ch_rate or abs(self.ma10_ch_rate) < self.ch_rate:
                    flag = 0
                    self.count = 0
                else:
                    print("\nM10 Ch:" + str(self.ma10_ch_rate) + "  " + "M20 Ch:" + str(self.ma20_ch_rate))
            if j == self.duration - 1 and flag == 1:
                print("SUCCESS!!! Downward " + ma10['time_key'][0]+ " " + str(self.count))
                self.count += 1
                return -1
        self.count = 0
        return 0

# Return Change Rate of MA10 and MA20
    def get_ma_ch_rate(self):
        return self.ma10_ch_rate, self.ma20_ch_rate

# Return MA Trend
    def get_ma_trend(self):
        return self.trend

# Get MA Trend Constantly
    def run(self):
        while 1:
            self.trend = self.detect()
            time.sleep(self.interval/1000)


class DetectRecover(threading.Thread):
    def __init__(self, qc, ma, duration = 5):
        super(DetectRecover, self).__init__()
        self.__quote_ctx = qc
        self.ma = ma
        self.duration = duration
        self.ref = 0

    def detect(self):
        ma1 = self.ma.get_get_ma_1m_data(self.duration)
        # 0,1,...,D-1
        ma1_value = [i for i in ma1["MA1"]]

        # Construct delta_MA1
        # 0,1,...,D-2
        delta_ma1 = []
        i = 0
        while i < self.duration - 1:
            delta_ma1.append(ma1_value[i+1]-ma1_value[i])
            i += 1
        print(delta_ma1)

        # Caculate Sum of increase, last one excluded
        i = 0
        sub_sum = 0
        while i < self.duration - 2:
            sub_sum += delta_ma1[i]
            i += 1

        # if sub sum is less than 0, it's not a upward trend. return
        if sub_sum <= 0:
            return 0

        # Find the reference
        if delta_ma1[self.duration < 0]:
            self.ref = ma1_value[self.duration - 2]
            print("refer: " + str(self.ref))

        # Detect recover
        if ma1_value[self.duration - 1] > self.ref:
            buy_price = ma1_value[self.duration - 1]
            print("BUY!!I WANT TO BUY!!" + str(buy_price))
            return 1

# Get MA Trend Constantly
    def run(self):
        while 1:
            ret = self.detect()
            time.sleep(5)
