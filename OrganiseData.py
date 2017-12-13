import numpy as np
import pandas as pd
import os
import glob

def parse_data(reverse_flag = False, replace_nan = True):
    ''' Parses the data from the tables from http://www.histdata.com/download-free-forex-data/?/ in the data folder into a single, binarized file.
    Set reverse_flag = False if you want to obtain rules for rising rates, and reverse_flag = True to obtain rules for falling rates'''

    prefix = "./data/"

    # we don't want to start from an empty dataframe or we run into labelling issues while joining

    df_all = pd.DataFrame([0])
    df_all.columns = [""]

    for dn in os.listdir(prefix):
        df_folder = pd.DataFrame()

        for fn in glob.glob(prefix + dn + "/" + "*.xlsx"):
            print("reading file : " + fn)
            df = pd.read_excel(fn)
            df.columns = ["date", "open", "high", "low", "close", "_"]
            df.set_index("date", inplace=True)
            df.drop(columns="_", inplace=True)

            # calculate the avg value as high-low/2 for each tick

            avg = (df["high"] - df["low"]) / 2

            # calculate the difference between two ticks

            diff = avg.diff()
            if reverse_flag:
                diff[diff > 0] = 1
                diff[diff < 0] = 0
            else:
                diff[diff > 0] = 0
                diff[diff < 0] = 1

            diff = pd.DataFrame(diff)
            diff.columns = [""]

            # concat all values from the folder

            df_folder = pd.concat([df_folder, diff])

        df_all = df_all.join(df_folder, how="outer", rsuffix=dn)

    # we have to remove the initial value we added for labeling issues

    df_all.drop(0, inplace=True)
    df_all.drop(columns="", inplace=True)


    #replace NaAs if flag is set

    if(replace_nan):
        df_all = df_all.fillna(0)

    # save into csv

    if reverse_flag:
        df_all.to_csv("./all_falling.csv", index_label="date", float_format="%d")
        print("saved everything to : all_falling.csv")
    else:
        df_all.to_csv("./all_rising.csv", index_label="date", float_format="%d")
        print("saved everything to : all_rising.csv")

def csv_to_arff(file_name):
    pass

parse_data(reverse_flag= False)

