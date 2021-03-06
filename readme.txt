Author : Blackliquid

Scripts to parse forex data to use with weka to formulate associative rules (eg. FpGrowth). Includes a live tracker that launches alerts when the live forex courses correspond to a pattern in a rule found by the algorithm.

OrganiseData.py : Parses the data files from http://www.histdata.com/download-free-forex-data/?/excel/1-minute-bar-quotes and writes it into a single csv file to use with weka. You have to put the xlsx files in e.g. ./data/2017/EUR_CHF.

ParseRules.py : Parses the rules found by Weka FPGrowth. Copy the rules into rules_rising_drop0.txt and rules_falling_drop0.txt for the live tracker

LiveTracker.py : Connects to live forex rates on http://webrates.truefx.com/rates/connect.html?f=html .

LiveAlerts.py : Uses LiveTracker to check for a mined pattern to emerge and give an alert

Instructions : 

1. Parse the training data into a csv file with drop = 0 parameter
2. Parse the test data into a csv file with drop = 3 parameter
2. Use Weka FpGrowth on the training data
3. Copy paste the generated Rules into rules_rising_drop0.txt or rules_falling_drop0.txt, according to the reverse_flag parameter in OrganiseData.py
4. Test the generated rules with TestAcc on the test set
4. Launch LiveAlerts.py for live alerts

Install dependencies : 

sudo pip3 install -r dependencies.txt
