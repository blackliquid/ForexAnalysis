from ParseRules import *
import numpy as np
import pandas as pd

def get_acc(prereq, conseq, records, test_interval = 1):
    alert_flag = False
    hits = []
    rates = []

    for record_row_index, record_row in records.iterrows():
        for prereq_row_index, prereq_row in prereq.iterrows():
            row_flag = True
            for entry_index, entry_value in prereq_row.iteritems():
                if ((entry_value == 1 and records.at[record_row_index, entry_index] == 0) or (
                        entry_value == 0 and records.at[record_row_index, entry_index] == 1)):
                    row_flag = False
            if (row_flag):
                #hits are saved in the format (record_row, rule_row)

                hits.append((record_row_index, prereq_row_index))

    num_records = test_data.count().values[0]
    true_positive = 0
    false_positive = 0

    for record_row, rule_row in hits:
        if(record_row < num_records-test_interval):
            true_prevision = True
            hit_rule = pd.DataFrame(conseq.iloc[rule_row, :])
            prediciton = hit_rule.idxmax().values[0]

            for i in range(1,test_interval+1):
                if(records.at[record_row+i, prediciton] == 0):
                    true_prevision = False

            if(true_prevision):
                true_positive += 1
            else:
                false_positive += 1



    return true_positive, false_positive


filename = "all_rising.csv"

test_data = pd.read_csv(filename)

prereq_rising, conseq_rising, _ = parse_rules("rules_rising.txt")
prereq_falling, conseq_falling, _ = parse_rules("rules_falling.txt")

tp, fp = get_acc(prereq_rising, conseq_rising, test_data)
acc = tp/(tp+fp)*100
print("Accuracy in % :", acc)

