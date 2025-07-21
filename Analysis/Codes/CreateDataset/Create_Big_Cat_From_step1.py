#ID des données art dans la catégorie -1 : 495
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df = pd.read_excel("../../Data/BT_step1_no_doublons.xlsx")

#rassembler toutes les données dans santé
df.loc[df["topic"] == 6,"topic"] = 2
df.loc[df["topic"] == 7,"topic"] = 2
df.loc[df["topic"] == 9,"topic"] = 2
df.loc[df["topic"] == 11,"topic"] = 2
df.loc[df["topic"] == 15,"topic"] = 2

#rassembler les données de la catégorie art
df.loc[df["topic"] == 17,"topic"] = 6
df.loc[df["topic"] == 18,"topic"] = 6
df.loc[df["ID"] == 495,"topic"] = 6

#décaler le reste des topic pour avoir des indices qui ce suivent

df.loc[df["topic"] == 8,"topic"] = 7
df.loc[df["topic"] == 10,"topic"] = 8
df.loc[df["topic"] == 12,"topic"] = -1
df.loc[df["topic"] == 13,"topic"] = 9
df.loc[df["topic"] == 14,"topic"] = 10
df.loc[df["topic"] == 15,"topic"] = 11
df.loc[df["topic"] == 16,"topic"] = 12

#Ajouter les autres étiquettes (émotions + science relatedness)
df_TER = pd.read_excel("../../../SciTweets-Emo.xlsx")
df = pd.merge(df,df_TER,on=["ID","text"])

df = df.sort_values("ID")
df.to_excel("../../Data/topicBigCat.xlsx",index=False)

print(df["topic"].value_counts())