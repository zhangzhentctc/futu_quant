from data_src.ma.GetMovingAverage import *
class DayReview:
    def __init__(self, qc):
        self.__quote_ctx = qc

    def review(self, t = 2, ch_rate = 0.8):
        ma = MovingAverage(self.__quote_ctx)
        ma10 = ma.get_ma_10m(765)
        ma20 = ma.get_ma_20m(765)
        ma50 = ma.get_ma_Xm(765, 50)
        # Condition 1 : Downward Trend
        #   1. Define T, around 10 mins
        #   2. During T,
        #        MA-10M[i] < MA-20M[i]
        #   3. During T
        #        delta

        print("**************************")
        count = 0

        i = 0
        i += 15
        while i < 765 - 420:
            flag = 1
            if ma10['MA10'][i] > ma20['MA20'][i]:
                for j in range(1, t):
                    flag = 1
                    # In case index is our of range
                    if i + j >= 765:
                        flag = 0
                        break
                    # Condition 1 MA Value Compare
                    if ma10['MA10'][i + j] <= ma20['MA20'][i + j]:
                        flag = 0
                        break
                    # Condition 2 MA Trend
                    if ma10['MA10'][i + j] - ma10['MA10'][i + j - 1] < 0 or ma20['MA20'][i + j] - ma20['MA20'][
                                        i + j - 1] < 0:
                        flag = 0
                        break
                # Condition 3 MA change rate
                if flag == 1:
                    ma10_ch_rate = (ma10['MA10'][i + t] - ma10['MA10'][i]) / t
                    ma20_ch_rate = (ma20['MA20'][i + t] - ma20['MA20'][i]) / t
                    if abs(ma20_ch_rate) < ch_rate:
                        flag = 0
                    else:
                        print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
                if j == t - 1 and flag == 1:
                    while 1:
                        if i + j >= 765:
                            break
                        if ma10['MA10'][i + j] <= ma20['MA20'][i + j]:
                            break
                        j += 1
                    print("SUCCESS!!! Upward ")
                    print(str(i) + " " + ma10['time_key'][i])
                    print("Duration:" + str(j))
                    count += 1
                    i += j

            if ma10['MA10'][i] < ma20['MA20'][i]:
                for j in range(1, t):
                    flag = 1
                    # In case index is our of range
                    if i + j >= 765:
                        flag = 0
                        break
                    # Condition 1 Value Compare
                    if ma10['MA10'][i + j] >= ma20['MA20'][i + j]:
                        flag = 0
                        break
                    # Condition 2 MA Trend
                    if ma10['MA10'][i + j] - ma10['MA10'][i + j - 1] > 0 or ma20['MA20'][i + j] - ma20['MA20'][
                                        i + j - 1] > 0:
                        flag = 0
                        break
                if flag == 1:
                    ma10_ch_rate = (ma10['MA10'][i + t] - ma10['MA10'][i]) / t
                    ma20_ch_rate = (ma20['MA20'][i + t] - ma20['MA20'][i]) / t
                    if abs(ma20_ch_rate) < ch_rate:
                        flag = 0
                    else:
                        print("\nM10 Ch:" + str(ma10_ch_rate) + "  " + "M20 Ch:" + str(ma20_ch_rate))
                if j == t - 1 and flag == 1:
                    while 1:
                        if i + j >= 765:
                            break
                        if ma10['MA10'][i + j] >= ma20['MA20'][i + j]:
                            break
                        j += 1
                    print("SUCCESS!!! Downward")
                    print(str(i) + " " + ma10['time_key'][i])
                    print("Duration:" + str(j))

                    count += 1
                    i += j

            i += 1

        print("Finished " + str(count))
        # Condition 2 : Upward Trend
        #   1. Define T, around 10 mins
        #   2. During T,
        #        MA-10M[i] > MA-20M[i]
        #   3. During T
        #        delta