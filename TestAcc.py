from ParseRules import *
import numpy as np
import pandas as pd

def test_acc(test_data, prereq, conseq):
    merge = pd.merge(prereq, test_data, how='inner')



filename = "all_rising.csv"

test_data = pd.read_csv(filename)

prereq_rising, conseq_rising = parse_rules("rules_rising.txt")
prereq_falling, conseq_falling = parse_rules("rules_falling.txt")