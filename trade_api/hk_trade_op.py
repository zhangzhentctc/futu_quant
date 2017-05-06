from trade_api.hk_trade_api import *
import time

class hk_trade_opt:
    def __init__(self, hk_trade_api):
        self.hk_trade_api = hk_trade_api

# envtype == 1 stands simulation
# envtype == 0 stands real trade
        self.envtype = 0
        self.place_time = 0

# Buy return:
# {'SvrResult': '0', 'Cookie': '888888', 'EnvType': '1', 'LocalID': '1425263522639675'}
    def buy(self, price, qty, strcode):
        cookie = "333"
        ret_code, ret_data = self.hk_trade_api.place_order(cookie, price, qty, strcode, 0, 0, self.envtype)
        if ret_code == -1:
            print("place order fail")
            return -1
        if ret_data["SvrResult"] == -1:
            print("buy fail")
            return -1
        if ret_data["Cookie"] != cookie:
            print("cookie check fail")
            return -1
        self.place_time = time.time()
        return ret_data["LocalID"]

    def sell(self,  price, qty, strcode):
        cookie = "444"
        ret_code, ret_data = self.hk_trade_api.place_order(cookie, price, qty, strcode, 1, 0, self.envtype)
        if ret_code == -1:
            print("place order fail")
            return -1
        if ret_data["SvrResult"] == -1:
            print("sell fail")
            return -1
        if ret_data["Cookie"] != cookie:
            print("cookie check fail")
            return -1
        return ret_data["LocalID"]

# order_list_query:
#  stock_code  stock_name dealt_avg_price dealt_qty localid orderid order_type  price status submited_time updated_time
# 0   67541  恒指法兴七八熊O.P   0.0  0  0  575219   0   0  0.06  7   1492965026   1492965026
# 1   67541  恒指法兴七八熊O.P   0.0  0  0  575220   0   1  0.06  7   1492965071   1492965071
    def get_order_id(self, localid):
        position = -1
        count = 0
        ret_code, ret_data = self.hk_trade_api.order_list_query("123", self.envtype)
        if ret_code == -1:
            return -1
        for i in ret_data["localid"]:
            if i == localid:
                position = count
                break
            count += 1

        if position == -1:
            print("warn: localid index fail")
            len = 0
            for index in ret_data.iterrows():
                len += 1

            if float(ret_data["submited_time"][len - 1]) - self.place_time < 10:
                position = len - 1
            else:
                position = -1
        if position == -1:
            print("check order id fail")
            return -1

        orderid = ret_data["orderid"][position]
        return orderid

    def check_order_status(self, orderid):
        cookie = "123"
        position = -1
        count = 0
        ret_code, ret_data = self.hk_trade_api.order_list_query(cookie, self.envtype)
        if ret_code == -1:
            return -1
        order_list = ret_data["orderid"]
        for i in order_list:
            if i == orderid:
                position = count
                break
            count += 1
        if position == -1:
            return -1
        return ret_data["status"][position]

    def disable_order(self, orderid):
        cookie = "555"
        ret_code, ret_data = self.hk_trade_api.set_order_status(cookie, 1, 0, orderid, self.envtype)
        if ret_code == -1:
            return -1
        if ret_data["SvrResult"] == -1:
            print("disable_order fail")
            return -1
        if ret_data["Cookie"] != cookie:
            print("cookie check fail")
            return -1
        return 1

    def get_dealt_qty(self, orderid):
        cookie = "654"
        position = -1
        count = 0
        dealt_qty = 0
        ret_code, ret_data = self.hk_trade_api.order_list_query(cookie, self.envtype)
        if ret_code == -1:
            return -1

        for i in ret_data["orderid"]:
            if i == orderid:
                position = count
                break
            count += 1

        if position == -1:
            print("get_dealt qty fail")
            return -1

        dealt_qty = ret_data["dealt_qty"][position]
        return dealt_qty

# Usage Examples
#    hk_trade = hk_trade_api()
#    hk_trade.initialize()
#    hk_trade.unlock_trade('88888888', '584679')
#    opt = hk_trade_opt(hk_trade)
#    localid = opt.buy(0.06, 10000, "67541")
#    orderid = opt.get_order_id(localid)
#    status = opt.check_order_status(orderid)
#    dealt = opt.get_dealt_qty(orderid)
#    print(dealt)
#    opt.disable_order(orderid)
