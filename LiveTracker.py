import urllib.request
import re
import numpy as np
import pandas as pd
import threading

def get_rates():
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

    # sub "/" for "_" for format unicity
    for i in range(len(split_text[:,0])):
        split_text[i, 0] = re.sub(r'/', r'_', split_text[i, 0])

    # convert to pandas dataframe

    df = pd.DataFrame(split_text)
    df.columns = ["currency", "timestamp", "bid_big_figure", "bid_pts", "offer_big_figure", "offer_pts", "high", "low", "open"]
    df.set_index("currency", inplace=True)

    return df

def binarize(table):
    diff = table["open"]-table["close"]
    diff[diff > 0] = 0
    diff[diff < 0] = 1
    diff = pd.DataFrame(diff, dtype=int)
    diff.columns = [""]
    return diff.transpose()

def print_loop():
    threading.Timer(interval,print_loop).start()
    df = get_rates()
    print(df)

interval = 1