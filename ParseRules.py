import re
import pandas as pd


def parse_rules(filename):
    '''Parses the rules found by weka saved in the rules.txt files'''

    file = open(filename)
    text = file.read()
    lines = re.split(r"\n", text)
    prereq = []
    conseq = []
    confidence = []

    for line in lines[0:-1]:
        temp_list = re.findall(r'\w\w\w_\w\w\w', line)
        prereq.append(temp_list[0:-1])
        conseq.append(temp_list[-1])
        confidence.append(re.search(r'<conf:\((\d.\d{1,2})\)', line).group(1))

    confidence_df = pd.DataFrame(confidence)

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
    for rule, conseq_iter in zip(prereq, conseq):
        onehot = pd.get_dummies(rule, columns= currencies)
        onehot = pd.DataFrame(onehot.sum(0))

        #add the condition that the consequence of the rule has to be 0. It's not interesting to know a rate is going to rise if it already rises

        onehot = pd.concat([onehot, pd.DataFrame([0], index = [conseq_iter])])
        prereq_binarized = pd.concat([prereq_binarized, onehot.transpose()])
    prereq_binarized.reset_index(inplace=True)
    prereq_binarized.drop(columns = "index", inplace=True)


    #binarize conseq

    conseq_binarized = pd.DataFrame(columns=currencies)
    for rule in conseq:
        onehot = pd.get_dummies(rule, columns=currencies)
        conseq_binarized = pd.concat([conseq_binarized, onehot])
    conseq_binarized.reset_index(inplace=True)
    conseq_binarized.drop(columns="index", inplace=True)
    conseq_binarized.fillna(0, inplace=True)

    #return prereq_df, conseq_df

    return prereq_binarized, conseq_binarized, confidence_df