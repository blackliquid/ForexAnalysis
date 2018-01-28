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


filename_rising = "./preprocessed/2017_rising_drop3.csv"
test_data_rising = pd.read_csv(filename_rising)

filename_falling = "./preprocessed/2017_falling_drop3.csv"
test_data_falling = pd.read_csv(filename_falling)

prereq_rising, conseq_rising, _ = parse_rules("./rules/rules_rising_drop0.txt")
prereq_rising.drop(columns = "AUD_USD", inplace = True)

prereq_falling, conseq_falling, _ = parse_rules("./rules/rules_falling_drop0.txt")
prereq_falling.drop(columns = "AUD_USD", inplace = True)

rising_tp, rising_fp = get_acc(prereq_rising, conseq_rising, test_data_rising)
falling_tp, falling_fp = get_acc(prereq_falling, conseq_falling, test_data_falling)

acc_rising = rising_tp/(rising_tp+rising_fp)*100
print(filename_rising+"Precision in % :", acc_rising)

acc_falling = falling_tp/(falling_tp+falling_fp)*100
print(filename_falling+"Precision in % :", acc_falling)