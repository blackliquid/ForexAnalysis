Author : Blackliquid

Scripts to parse forex data to use with weka to formulate associative rules (eg. FpGrowth). Includes a live tracker that launches alerts when the live forex courses correspond to a pattern in a rule found by the algorithm.

OrganiseData.py : Parses the data files from http://www.histdata.com/download-free-forex-data/?/excel/1-minute-bar-quotes and writes it into a single csv file to use with weka.

ParseRules.py : Parses the rules found by Weka FPGrowth. Copy the rules into rules.txt.

LiveTracker.py : Connects to live forex rates on http://webrates.truefx.com/rates/connect.html?f=html .

LiveAlerts.py : Uses LiveTracker to check for a mined pattern to emerge and give an alert

Instructions : 

1. Parse the historical data into all.csv
2. Use Weka FpGrowth on all.csv
3. Copy paste the generated Rules into ParseRules.py
4. Launch LiveAlerts.py