import numpy as np
import pandas as pd
import os
import glob

prefix = "./data/"

#we don't want to start from an empty dataframe or we run into labelling issues while joining

df_all = pd.DataFrame([np.nan])
df_all.columns = [""]


for dn in os.listdir(prefix):
    df_folder = pd.DataFrame()

    for fn in glob.glob(prefix+dn+"/"+"*.xlsx"):
        print("reading file : " + fn)
        df = pd.read_excel(fn)
        df.columns = ["date", "open", "high", "low", "close", "_"]
        df.set_index("date", inplace=True)
        df.drop(columns="_", inplace=True)

        #set value to 1 if the rate went up while the tick and 0 else

        diff = df["open"] - df["close"]
        diff[diff > 0] = 0
        diff[diff < 0] = 1
        diff = pd.DataFrame(diff)
        diff.columns = [""]

        #concat all values from the folder

        df_folder = pd.concat([df_folder, diff])

    df_all = df_all.join(df_folder, how="outer", rsuffix=dn)

#we have to remove the initial value we added for labeling issues

df_all.drop(0, inplace = True)
df_all.drop(columns = "", inplace = True)


#save into csv

df_all.to_csv("./all.csv", index_label = "date")
print("saved everything to : all.csv")