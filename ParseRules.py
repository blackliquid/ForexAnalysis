import re
import pandas as pd


file = open("rules.txt")
text = file.read()

def parse_rules():
    lines = re.split(r"\n", text)
    clean_lines = []

    for line in lines[0:-1]:
        clean_lines.append(re.sub(r'binarized', r'-', re.sub(r'\W|[0-9]|confliftlevconv', r'', line)))

    prereq = []
    conseq = []

    for line in clean_lines:
        temp_list = re.split(r"-", line)

        temp_list_clean = []

        for elem in temp_list[0:-1]:
            temp_list_clean.append(elem[:-1])
        prereq.append(temp_list_clean[0:-1])
        conseq.append(temp_list_clean[-1])



    #binarize attributes

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

    #binarize prereq

    prereq_binarized = pd.DataFrame(columns=currencies)
    for rule in prereq:
        onehot = pd.get_dummies(rule, columns= currencies)
        onehot = pd.DataFrame(onehot.sum(0))
        prereq_binarized = pd.concat([prereq_binarized, onehot.transpose()])
    prereq_binarized.reset_index(inplace=True)
    prereq_binarized.drop(columns = "index", inplace=True)
    prereq_binarized.fillna(0, inplace=True)


    #binarize conseq

    conseq_binarized = pd.DataFrame(columns=currencies)
    for rule in conseq:
        onehot = pd.get_dummies(rule, columns=currencies)
        conseq_binarized = pd.concat([conseq_binarized, onehot])
    conseq_binarized.reset_index(inplace=True)
    conseq_binarized.drop(columns="index", inplace=True)
    conseq_binarized.fillna(0, inplace=True)

    #return prereq_df, conseq_df

    return prereq_binarized, conseq_binarized