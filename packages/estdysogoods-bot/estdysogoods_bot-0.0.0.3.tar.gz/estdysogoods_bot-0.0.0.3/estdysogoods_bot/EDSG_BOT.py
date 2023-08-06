from iqoptionapi.stable_api import IQ_Option
import numpy as np
import time
import hashlib
class EDSG_BOT():
    def __init__(self,password_bot,user,password):
        self.user = user
        self.password = password
        self.password_bot = password_bot

    def HASHPASS(self,hash_password):
            return hashlib.md5(hash_password.encode()).hexdigest()

    def botiq_sma_cut(self):
        password_bot = self.HASHPASS(self.password_bot)

        if password_bot == "7574e33be1ec341ec3791c9c9aefcbe6":
            pass
        else:
            print("Check password bot!")
            time.sleep(10)
            quit()

        user = self.user
        password = self.password
        API = IQ_Option(user,password)
        check_connect,_ = API.connect()



        profit = 0.0
        win = 0
        loss = 0

        RMG = 0



        if check_connect == True:
            print("Login..")
        else:
            print("Check user or password !")
            time.sleep(10)
            quit()

        print("TYPE = 1.REAL // 2.DEMO")
        mode_ac = int(input("TYPE :"))
        if mode_ac == 1:
            API.change_balance("REAL")
        else:
            pass

        print(f"Balance :{API.get_balance()}{API.get_currency()}")
        ATM = float(input("Amount :"))
        reset_amount = ATM
        RT = int(input("Duration :"))
        currency_pair = input("Currency pair :")
        TF = int(input("Time frame :"))

        mode_martingale = input("Mode martingale :")
        multiply_martingale = float(input("Multiply martingale :"))
        max_round_martingale = int(input("Max round martingale :"))

        while True:
            TP = float(input("TP :"))
            SL = float(input("SL :"))
            if SL > 0:
                print("Error SL // ex SL = -100")
            else:
                break


        SMAFAST = int(input("SMA FAST :"))
        SMASLOW = int(input("SMA SLOW :"))

        def wing_lossg(get_mode,get_rs,get_atm,get_reset_amount,get_qmg,get_maxgm,get_rmg,get_win,get_loss,get_profit):
                if get_mode == "loss":
                    if get_rs > 0:
                        get_win = get_win + 1
                        get_atm = get_reset_amount
                        get_profit = get_profit + get_rs
                        get_rmg = 0

                    elif get_rs < 0:
                        get_loss = get_loss + 1
                        get_atm = get_atm * get_qmg
                        get_profit = get_profit + get_rs

                        get_rmg = get_rmg + 1

                        if get_maxgm < get_rmg:
                            get_atm = get_reset_amount
                            get_rmg = 0

                elif get_mode == "win":
                    if get_rs > 0:
                        get_win = get_win + 1
                        get_atm = get_atm * get_qmg
                        get_profit = get_profit + get_rs

                        get_rmg = get_rmg + 1

                        if get_maxgm < get_rmg:
                            get_atm = get_reset_amount
                            get_rmg = 0

                    elif get_rs < 0:
                        get_loss = get_loss + 1
                        get_atm = get_reset_amount
                        get_profit = get_profit + get_rs
                        get_rmg = 0

                return get_atm,get_rmg,get_win,get_loss,get_profit
        def datas_ca():
            global currency_pair,TF
            data_ca = API.get_candles(currency_pair,TF,1000,API.get_server_timestamp())
            close = np.array([])
            for data_cas in data_ca:
                close = np.append(close,data_cas["close"])
            return close
        def SMA(close,input_period):
            j = next(i for i, x in enumerate(close) if x is not None)
            our_range = range(len(close))[j + input_period - 1:]
            empty_list = [None] * (j + input_period - 1)
            sub_result = [np.mean(close[i - input_period + 1: i + 1]) for i in our_range]

            return np.array(empty_list + sub_result)


        type_acs = API.get_currency()

        while True:

            print(f"Profit :{'%.2f'%profit}{type_acs} // win :{win} // loss :{loss}")

            if profit >= TP:
                print(f"STOP TP {'%.2f'%profit}{type_acs}")
                time.sleep(60*10)
                quit()
            elif profit <= SL:
                print(f"STOP SL {'%.2f'%profit}{type_acs}")
                time.sleep(60*10)
                quit()

            close = datas_ca()
            data_sma_fast = SMA(close,SMAFAST)[-1]
            data_sma_slow = SMA(close,SMASLOW)[-1]

            if data_sma_fast > data_sma_slow:
                while True:
                    close = datas_ca()
                    data_sma_fast = SMA(close,SMAFAST)[-1]
                    data_sma_slow = SMA(close,SMASLOW)[-1]
                    if data_sma_fast < data_sma_slow:
                        order_buy,id_buy = API.buy(ATM,currency_pair,"call",RT)
                        if order_buy == True:
                            profit_buy = API.check_win_v3(id_buy)
                            ATM,RMG,win,loss,profit = wing_lossg(mode_martingale,profit_buy,ATM,reset_amount,multiply_martingale,max_round_martingale,RMG,win,loss,profit)
                            break
                        else:
                            break
            elif data_sma_fast < data_sma_slow:
                while True:
                    close = datas_ca()
                    data_sma_fast = SMA(close,SMAFAST)[-1]
                    data_sma_slow = SMA(close,SMASLOW)[-1]
                    if data_sma_fast > data_sma_slow:
                        order_sell,id_sell = API.buy(ATM,currency_pair,"call",RT)
                        if order_sell == True:
                            profit_sell = API.check_win_v3(id_sell)
                            ATM,RMG,win,loss,profit = wing_lossg(mode_martingale,profit_sell,ATM,reset_amount,multiply_martingale,max_round_martingale,RMG,win,loss,profit)
                            break
                        else:
                            break

