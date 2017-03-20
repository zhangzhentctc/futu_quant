from data_src.ma.GetMovingAverage import *

class DetectSignal:
    def __init__(self, qc):
        self.__quote_ctx = qc
        self.count = 0

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
    def detect(self, t=2, ch_rate = 0.8):
        flag = 1

        ma = MovingAverage(self.__quote_ctx)
        ma10 = ma.get_ma_10m(t)
        ma20 = ma.get_ma_20m(t)

        # Check Upward Trend
        if ma10['MA10'][0] > ma20['MA20'][0]:
            for j in range(1, t):
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
                ma10_ch_rate = (ma10['MA10'][t - 1] - ma10['MA10'][0]) / t
                ma20_ch_rate = (ma20['MA20'][t - 1] - ma20['MA20'][0]) / t
                if abs(ma20_ch_rate) < ch_rate or abs(ma10_ch_rate) < ch_rate :
                    flag = 0
                    self.count = 0
                else:
                    print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
            if j == t - 1 and flag == 1:
                print("SUCCESS!!! Upward " + ma10['time_key'][0] + " " + str(self.count))
                self.count += 1
                return 1

        # Check Downward Trend
        if ma10['MA10'][0] < ma20['MA20'][0]:
            for j in range(1, t):
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
                ma10_ch_rate = (ma10['MA10'][t - 1] - ma10['MA10'][0]) / t
                ma20_ch_rate = (ma20['MA20'][t - 1] - ma20['MA20'][0]) / t
                if abs(ma20_ch_rate) < ch_rate or abs(ma10_ch_rate) < ch_rate:
                    flag = 0
                    self.count = 0
                else:
                    print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
            if j == t - 1 and flag == 1:
                print("SUCCESS!!! Downward " + ma10['time_key'][0]+ " " + str(self.count))
                self.count += 1
                return -1
        self.count = 0
        return 0