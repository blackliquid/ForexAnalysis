import numpy as np
import pandas as pd
import os
import glob

def parse_data(folder, reverse_flag = False, replace_nan = False, drop = 1):
    ''' Parses the data from the tables from http://www.histdata.com/download-free-forex-data/?/ in the data folder into a single, binarized file.
    Set reverse_flag = False if you want to obtain rules for rising rates, and reverse_flag = True to obtain rules for falling rates'''

    prefix = "./data/"+folder+"/"

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

            # concat all values from the folder

            df_folder = pd.concat([df_folder, avg])

        df_folder.columns = [""]
        df_all = df_all.join(df_folder, how="outer", rsuffix=dn)

    #if drop activated, only keep 1/drop of the columns

    if (drop != 0 and drop != 1):
        df_all.reset_index(inplace=True)
        df_all.drop(list(set(range(0, len(df_all.index))) - set(range(0, len(df_all.index), drop))), inplace=True)
        df_all.set_index("index", inplace=True)

     # we have to remove the initial value we added for labeling issues

    df_all.drop(columns="", inplace=True)

    #make the diff

    diff = df_all.diff()

    if reverse_flag:
        diff[diff > 0] = 0
        diff[diff < 0] = 1
    else:
        diff[diff > 0] = 1
        diff[diff < 0] = 0



    #replace NaAs if flag is set

    if(replace_nan):
        diff = df_all.fillna(0)

    # save into csv

    if reverse_flag:
        diff.to_csv("./"+folder+"_falling_drop"+str(drop)+".csv", index_label="date", float_format="%d")
        print("./"+folder+"_falling_drop"+str(drop)+".csv")
    else:
        diff.to_csv("./"+folder+"_rising_drop"+str(drop)+".csv", index_label="date", float_format="%d")
        print("./"+folder+"_rising_drop"+str(drop)+".csv")

def csv_to_arff(file_name):
    pass

folder = "2017"
parse_data(folder, reverse_flag= True, drop = 0)

