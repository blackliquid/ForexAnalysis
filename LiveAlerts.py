from ParseRules import *
from LiveTracker import *
from pygame import mixer
import datetime
import pandas as pd
import threading


class LiveAlert(LiveTracker):
    def __init__(self, print_interval = 1, update_interval = 1, avg_interval = 60):
        '''print_interval : interval for printing the rates for the print_loop method
        update_interval : time interval for fetching the data from truefx
        average_interval : interval for taking the average of the rate (the history is given in 1min Intervals, so it makes sense to set it to 60)'''

        self.update_interval = update_interval
        self.print_interval = print_interval
        self.avg_interval = avg_interval
        self.connected_print_flag = True
        self.init_flag = False
        self.avg = None
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

        #parse rules from rules_rising.txt / rules_falling.txt

        self.prereq_rising, self.conseq_rising, self.confidence_rising = parse_rules("rules_rising.txt")
        self.prereq_falling, self.conseq_falling, self.confidence_falling = parse_rules("rules_falling.txt")


    def alert_loop(self):
        '''method for giving automated warning in case that a mined rule is detected'''

        threading.Timer(self.update_interval, self.alert_loop).start()

        #collect the data every update_interval

        rates = self.get_rates()

        if rates is not None:
            self.rates_list.append(self.get_rates())

        #average the adata every avg_interval

        if len(self.rates_list) == self.avg_interval:
            self.avg_old = self.avg
            self.avg = self.get_avg(self.rates_list)
            self.rates_list = []

            #we only can start comparing after we collected twovalues

            if self.init_flag == True:
                diff_rising = self.binarize()
                diff_falling = self.binarize(reverse_flag=True)

                alert_flag_rising, date_rising, prediction_rising, pred_conf_rising = self.compare_with_nan(self.prereq_rising, self.conseq_rising, diff_rising, self.confidence_rising)
                alert_flag_falling, date_falling, prediction_falling, pred_conf_falling = self.compare_with_nan(self.prereq_falling, self.conseq_falling, diff_falling, self.confidence_falling)

                #if some rule rising/falling rule matches, give alert

                if(alert_flag_rising is True):
                    self.audio_alert()
                    print(date_rising)
                    for curr, conf in zip(prediction_rising, pred_conf_rising):
                        print("Prediction : " + curr + " rising with confidence " + conf)

                if (alert_flag_falling is True):
                    self.audio_alert()
                    print(date_falling)
                    for curr, conf in zip(prediction_falling, pred_conf_falling):
                        print("Prediction : " + curr + " falling with confidence " + conf)

            self.init_flag = True

    def binarize(self, reverse_flag = False):
        '''Outputs the binarized difference vector between two ticks to see if the rate went up or down.
         reverse_flag = False : 1 => rate went up; 0 => rate went down
         reverse_flag = True : 1 => rate went up; 0 => rate went down'''

        diff = self.avg_old["bid"] - self.avg["bid"]

        if reverse_flag:
            diff[diff > 0] = 1
            diff[diff < 0] = 0
        else:
            diff[diff > 0] = 0
            diff[diff < 0] = 1

        diff = pd.DataFrame(diff, dtype=int)
        diff.columns = ["live"]

        return diff.transpose()

    def get_avg(self,rates_list):
        return sum(rates_list) / len(rates_list)

    def compare(self,prereq, conseq, live_bin):
        '''This method compares the live data to the rules mined via a inner join to see if any rule matches
        Returns a tuple (alert_flag, datetime, prediciton_string) where alert_flag is True when a rule is matched'''

        alert_flag = False
        rate = []

        #so we can track which rule was applied we add an column with the indices which can be tracked later
        prereq = prereq.reset_index()

        merge = pd.merge(prereq, live_bin, on=self.currencies, how='inner')

        for i in range(len(merge)):
            alert_flag = True

        if len(merge) > 0 :
            alert_flag = True
            hits = merge["index"]

            for i in hits.values:
                hit_conseq = pd.DataFrame(conseq.iloc[i, :])
                hit_rate = hit_conseq.idxmax().values[0]
                rate.append(hit_rate)

        return (alert_flag, datetime.datetime.now(), rate)

    def compare_with_nan(self, prereq, conseq, record, confidence):

        alert_flag = False
        hits = []
        rates = []
        confidence_list = []

        for prereq_row_index, prereq_row in prereq.iterrows():
            row_flag = True
            for entry_index, entry_value in prereq_row.iteritems():
                if(entry_value == 1 and record.at["live",entry_index] == 0):
                    row_flag = False
            if(row_flag):
                hits.append(prereq_row_index)
                confidence_list.append(confidence.iloc[prereq_row_index].item())

        if(len(hits)>0):
            alert_flag = True
            for i in hits:
                hit_conseq = pd.DataFrame(conseq.iloc[i, :])
                hit_rate = hit_conseq.idxmax().values[0]
                rates.append(hit_rate)

        return alert_flag, datetime.datetime.now(), rates, confidence_list

    def audio_alert(self):
        mixer.init()
        mixer.music.load('alert.mp3')
        mixer.music.play()

live_alert = LiveAlert()
live_alert.alert_loop()
print("Checking live rates and checking for matching rules...")
