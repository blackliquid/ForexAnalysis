from ParseRules import *
from LiveTracker import *
import threading

def alert_loop():
    threading.Timer(interval,alert_loop).start()
    rates = get_rates()
    compare(prereq, conseq, rates)
    print("tick")

def compare(prereq, conseq, rates):
    live_bin = binarize(rates)
    merge = pd.merge(prereq, live_bin, on=currencies, how='inner')

    for i in range(len(merge)):
        hit_index = merge.iloc[i, -1]
        live_conseq = pd.DataFrame(conseq.iloc[5, :])
        prediction = live_conseq.idxmax().values[0]
        print("Prediction : " + prediction + " rising")

currencies = ["EUR_USD",
    "USD_JPY",
    "GBP_USD",
    "EUR_GBP",
    "USD_CHF",
    "EUR_JPY",
    "EUR_CHF",
    "USD_CAD",
    "AUD_USD",
    "GBP_JPY"]

interval = 1

prereq, conseq = parse_rules(text)
alert_loop()