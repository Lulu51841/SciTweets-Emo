import pandas as pd
import numpy as np
import modèles.scitweets_classifier as Sc

def somme(liste):
    _somme = 0
    for i in liste:
        _somme = _somme + i
    return _somme

Eckman = ['peur','colère','joie','surprise','tristesse','dégoût','neutre']

df_anger = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Anger_anon.csv",sep=",")
df_disgust = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Disgust_anon.csv",sep=",")
df_fear = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Fear_anon.csv",sep=",")
df_joy = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Joy_anon.csv",sep=",")
df_Sadness = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Sadness_anon.csv",sep=",")
df_Trust = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Trust_anon.csv",sep=",")
df_anticipation = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Anticipation_anon.csv",sep=",")
df_surprise = pd.read_csv("../../Data/CancerEmo/CancerEMODataset/Surprise_anon.csv",sep=",")

Liste_df = [df_fear,df_anger,df_joy,df_surprise,df_Sadness,df_disgust]
list_snd_col = ["Fear","Anger","Joy","Surprise","Sadness","Disgust"]
df_merge = pd.DataFrame({"text": df_fear.iloc[0]["Sentence"],"emotions": [[0,0,0,0,0,0]]})

already_In = [df_fear.iloc[0]["Sentence"]]
i = 0
for df in Liste_df:
    for index, row in df.iterrows():
        if row["Sentence"] in already_In :
            if(i > 0):
                if not already_In:
                    print("Empty list")
            if(row[list_snd_col[i]] == 1):
                l = list(df_merge.loc[df_merge.index[df_merge["text"] == row["Sentence"]],"emotions"])[0]
                l[i] = 1
                df_merge.loc[df_merge.index[df_merge["text"] == row["Sentence"]][0],"emotions"] = l
        else:
            l = [0]*6
            if(row[list_snd_col[i]] == 1):
                l[i] = 1
            df_merge = pd.concat([pd.DataFrame({"text" : row["Sentence"], "emotions" : [l]}), df_merge], ignore_index=True)
            already_In.append(row["Sentence"])
    i+=1


for index, row in df_merge.iterrows():
    if somme(row["emotions"]) > 1:
        print("on est bon")
        df_merge.to_csv("../../Data/CancerEmo/CancerEMODataset/merged_dataset.tsv",sep="\t")
        df = Sc.transform(df_merge,"../../Data/CancerEmo/CancerEMODataset/Cancer_Science_related.tsv")
        df["scientific_claim"] = df.apply(lambda x: round(x["cat1_score"]), axis=1)
        df["scientific_reference"] = df.apply(lambda x: round(x["cat2_score"]), axis=1)
        df["scientific_context"] = df.apply(lambda x: round(x["cat3_score"]), axis=1)
        df["science_related"] = df.apply(lambda x: 1 if (x["scientific_claim"] == 1 or x["scientific_reference"] == 1 or x["scientific_context"] == 1) else 0, axis=1)
        df_final = df[["text","emotions","science_related","scientific_claim","scientific_reference","scientific_context"]]
        df_final.to_excel("../../Data/CancerEmo/CancerEmo_Sci.xlsx",index=False)
        exit()
print("toujours pas")




