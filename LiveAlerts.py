from ParseRules import *
from LiveTracker import *
import datetime
import pandas as pd
import threading


class LiveAlert(LiveTracker):
    def __init__(self):
        self.init_flag = False
        self.avg = None

        #time interval for fetching the data from truefx

        self.update_interval = 1

        #interval for printing the rates for the print_loop method

        self.print_interval = 1

        #interval for taking the average of the rate (the history is given in 1min Intervals, so it makes sense to set it to 60)

        self.avg_interval = 60

        self.counter = 0
        self.currencies = ["EUR_USD",
                           "USD_JPY",
                           "GBP_USD",
                           "EUR_GBP",
                           "USD_CHF",
                           "EUR_JPY",
                           "EUR_CHF",
                           "USD_CAD",
                           "AUD_USD",
                           "GBP_JPY"]
        self.rates_list = []
        self.prereq, self.conseq = parse_rules()

    def alert_loop(self):
        '''method for giving automated warning in case that a mined rule is detected'''

        threading.Timer(self.update_interval, self.alert_loop).start()

        #collect the data every update_interval

        self.rates_list.append(self.get_rates())

        #average the adata every avg_interval

        if len(self.rates_list) == self.avg_interval:
            self.avg_old = self.avg
            self.avg = self.get_avg(self.rates_list)
            self.rates_list = []

            #we only can start comparing after we collected twovalues

            if self.init_flag == True:
                diff = self.get_diff()
                self.compare(self.prereq, self.conseq, diff)

            self.init_flag = True

    def get_diff(self):
        '''outputs the binarized difference vector between two ticks to see if the rate went up or down. 1-> rate went up; 0-> rate went down'''

        diff = self.avg_old["bid"]-self.avg["bid"]
        diff[diff > 0] = 0
        diff[diff < 0] = 1
        diff = pd.DataFrame(diff, dtype=int)
        diff.columns = [""]
        return diff.transpose()

    def get_avg(self,rates_list):
        return sum(rates_list) / len(rates_list)

    def compare(self,prereq, conseq, live_bin):
        '''this method compares the live data to the rules mined via a inner join to see if any rule matches'''

        merge = pd.merge(prereq, live_bin, on=self.currencies, how='inner')

        for i in range(len(merge)):
            hit_index = merge.iloc[i, -1]
            live_conseq = pd.DataFrame(conseq.iloc[5, :])
            prediction = live_conseq.idxmax().values[0]
            print(datetime.datetime.now())
            print(" Prediction : " + prediction + " rising")

live_alert = LiveAlert().alert_loop()
