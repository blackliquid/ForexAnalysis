import urllib.request
import re
import numpy as np
import pandas as pd
import threading

class LiveTracker():
    def __init__(self):
        self.print_interval = 1

    def get_rates(self):
        ''''fetches the rates from truefx'''

        # open webpage

        webpage = urllib.request.urlopen("http://webrates.truefx.com/rates/connect.html?f=html")

        # decode with utf8

        text = webpage.read().decode("utf-8")

        # simple dirty parsing with regex

        split_text = re.split(r'</td><td>|<table><tr><td>|</td></tr><tr><td>|</td></tr></table>\r\n', text)
        split_text.__delitem__(0)
        split_text.__delitem__(len(split_text) - 1)

        # split text and reshape

        split_text = np.reshape(split_text, [10, 9])
        split_text_joined = []

        # sub "/" for "_" for format unicity
        for i in range(len(split_text[:, 0])):
            split_text[i, 0] = re.sub(r'/', r'_', split_text[i, 0])
            split_text_joined.append([split_text[i,0], split_text[i,1], split_text[i,2]+split_text[i,3], split_text[i,4]+split_text[i,5], split_text[i,6], split_text[i,7], split_text[i,8]])

        # convert to pandas dataframe

        columns = ["currency", "timestamp", "bid", "offer", "high", "low",
                   "open"]
        df = pd.DataFrame(split_text_joined, columns=columns)
        df.set_index("currency", inplace=True)
        df = df.astype(float)

        return df

    def print_loop(self):
        '''prints the current rate every print_interval'''

        threading.Timer(self.print_interval, self.print_loop).start()
        df = self.get_rates()
        print(df)