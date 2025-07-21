from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
import pickle
import pandas as pd
import numpy as np

df = pd.read_excel("../../Data/BerTopic_step1.xlsx")

print(df.columns)

ID_list = []
doublons = []

for indew, row in df.iterrows():
    if row["ID"] in ID_list:
        doublons.append(row["ID"])
    else:
        ID_list.append(row["ID"])

print(len(ID_list))
print(len(doublons))
print(doublons)

def sortDoublons(x):
    if x["ID"] in doublons :
        return x

def priveDe(list1,list2):
    listRes = []
    for e in list1:
        if not(e in list2):
            listRes.append(e)
    return listRes

def insert(df, row):
    insert_loc = df.index.max()

    if pd.isna(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row

dfTopic = df[df["ID"].isin(doublons)]

dfTopic.to_excel('../../Data/browse/step2/doublons.xlsx',index=False)

df_no_doublons = df[df["ID"].isin(priveDe(ID_list,doublons))]
print(df_no_doublons.shape)

trace = priveDe(ID_list,doublons)
for index, row in df.iterrows():
    if not (row["ID"] in trace):
        trace.append(row["ID"])
        insert(df_no_doublons,row)

df_no_doublons.to_excel("../../Data/BT_step1_no_doublons.xlsx",index=False)