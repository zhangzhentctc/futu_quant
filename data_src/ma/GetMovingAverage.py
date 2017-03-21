from openft.open_quant_context import *

##
# Get Real-Time Moving Average
# Return :
#    pd Dataframe
#    format: MAx, time_key
##


class MovingAverage:
    def __init__(self, qc):
        self.__quote_ctx = qc

    def get_ma_1m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                # Make Data List
                ma1_value_list= []
                for unit in kline_table["close"]:
                    ma1_value_list.append(unit)

               # make time list
                time_list = []
                for unit in kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA1": ma1_value_list[i], "time_key": time_list[i]})
                ma_1m_table = pd.DataFrame(data, columns=["MA1", "time_key"])

                return ma_1m_table

    def get_ma_10m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + 9, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[9: 10 + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= 9:
                        tmp_sum = 0
                        for j in range(0, 10):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / 10
                    count = count + 1

                # abandon the first 9 numbers
                ma10_value_list = whole_value_list[9:9+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA10": ma10_value_list[i], "time_key": time_list[i]})
                ma_10m_table = pd.DataFrame(data, columns=["MA10", "time_key"])

                return ma_10m_table

    def get_ma_20m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + 19, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[19: 20 + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= 19:
                        tmp_sum = 0
                        for j in range(0, 20):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / 20
                    count = count + 1

                # abandon the first 9 numbers
                ma20_value_list = whole_value_list[19:19+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA20": ma20_value_list[i], "time_key": time_list[i]})
                ma_20m_table = pd.DataFrame(data, columns=["MA20", "time_key"])

                return ma_20m_table

    def get_ma_Xm(self, number, x):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for sub_type in sub_type_list:
                ret_status, ret_data = self.__quote_ctx.subscribe(code, sub_type)
                if ret_status != RET_OK:
                    print("%s %s: %s" % (code, sub_type, ret_data))
                    exit()

        ret_status, ret_data = self.__quote_ctx.query_subscription()

        if ret_status == RET_ERROR:
            print(ret_data)
            exit()

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number + x-1, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    exit()
                kline_table = ret_data

                sub_kline_table = kline_table
                sub_kline_table = sub_kline_table[x-1: x + number]
                # make whole value list
                whole_value_list= []
                for unit in kline_table["close"]:
                    whole_value_list.append(unit)

                repli_whole_value_list = [i for i in whole_value_list]
                # Caculate MA
                count = 0
                for i in whole_value_list:
                    if count >= x-1:
                        tmp_sum = 0
                        for j in range(0, x):
                            tmp_sum = tmp_sum + repli_whole_value_list[count - j]
                        whole_value_list[count] = tmp_sum / x
                    count = count + 1

                # abandon the first 9 numbers
                ma_value_list = whole_value_list[x-1:x-1+number]

                # make time list
                time_list = []
                for unit in sub_kline_table["time_key"]:
                    time_list.append(unit)

                # Combine data
                data = []
                for i in range(0, number ):
                    data.append({"MA-x": ma_value_list[i], "time_key": time_list[i]})
                ma_x_table = pd.DataFrame(data, columns=["MA-x", "time_key"])

                return ma_x_table