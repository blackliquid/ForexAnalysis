from ParseRules import *
import numpy as np
import pandas as pd

def get_acc(prereq, conseq, records):
    '''Tests the accuracy of a set of rules on historical data.'''

    alert_flag = False
    hits = []
    rates = []

    for record_row_index, record_row in records.iterrows():
        for prereq_row_index, prereq_row in prereq.iterrows():
            row_flag = True
            for entry_index, entry_value in prereq_row.iteritems():
                if ((entry_value == 1 and records.at[record_row_index, entry_index] == 0) or (
                        entry_value == 0 and records.at[record_row_index, entry_index] == 1) or ((not np.isnan(entry_value) and np.isnan(records.at[record_row_index, entry_index])))):
                    row_flag = False
            if (row_flag):
                # hits are saved in the format (record_row, rule_row)

                hits.append((record_row_index, prereq_row_index))
    num_records = records.shape[0]
    true_positive = 0
    false_positive = 0
    checks = []

    for record_row, rule_row in hits:
        if(record_row < num_records-1):
            hit_rule = pd.DataFrame(conseq.iloc[rule_row, :])
            prediction = hit_rule.idxmax().values[0]

            if(records.at[record_row + 1, prediction] == 1):
                true_positive += 1
                checks.append(1)
            if(records.at[record_row + 1, prediction] == 0):
                false_positive += 1
                checks.append(0)

    return true_positive, false_positive


filename = "2017_01_rising_drop3.csv"

real_data = pd.read_csv(filename)

prereq_rising, conseq_rising, _ = parse_rules("rules_rising.txt")
prereq_rising.drop(columns = "AUD_USD", inplace = True)
#prereq_falling, conseq_falling, _ = parse_rules("rules_falling.txt")
#prereq_falling.drop(columns = "AUD_USD", inplace = True)

tp, fp = get_acc(prereq_rising, conseq_rising, real_data)
acc = tp/(tp+fp)*100
print(filename+" Accuracy in % :", acc)