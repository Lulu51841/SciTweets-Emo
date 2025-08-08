import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from pathlib import Path

Ekman = ['fear','anger','joy','surprise','sadness','disgust','neutral']

def getLastIn(df,column,percent=0.2):
    if(percent > 1):
        print("please choose a number smaller than 1 and greater than 0")
        return -1
    df = df.sort_values(column,ascending=False)
    somme = df[column].sum()
    total = 0
    cpt=0
    for index, row in df.iterrows():
        total += row[column]
        if(total/somme > percent):
            return (index,row[column],(row[column]/somme)*100)
        cpt+=1

def to_ternary(n):
    ternary=np.base_repr(n,base=3)
    result = []
    while n > 0:
        result.append(n % 3)
        n = n // 3
    while len(result) < 2:
        result.append(0)
    result = result[::-1]
    return result

def compute_percents(df,column):
    try :
        df[column]
    except KeyError:
        print("Cette colonne n'existe pas")
        return -1
    som = df[column].sum()
    df[str(column)+"_percent"] = df.apply(lambda x: (x[column]/som)*100,axis=1)
    return df

def compute_signature(df,labels,save=False,plot=True):
    #df  -> path to the file containing the data extracted by SEANCE you want to compute the signature with
    #labels -> list of string containing the labels for each line of the file ("/../../Graphs/SciTweetsGraph/FeaturesAnalysis/Signature/" for the current directory used to store SEANCE signature)
    #save -> False if you dont want to save the graphs, else write the path to the directory you want to save the signature in
    #plot -> True if you want to plot the graph, else False
    if(type(df) == str):
        df = pd.read_csv(df)

    columns = df.columns
    dico = columns[2].split("_")[1].replace("'","")
    stop = True ; indice = -1; i = 0
    while stop and i<len(columns):
        if "_neg_3" in columns[i]:
            indice = i
            stop = False
        i+=1
    if( indice !=-1):
        df = df[df.columns[:indice]]
    df = df.T
    df.columns = labels
    df = df.iloc[2:]

    Limites = {}
    df["to_plot"] = 0
    for e in labels:
        df = compute_percents(df,e)
        index,w,limite = getLastIn(df,e,0.50)
        print(limite)
        Limites[e] = limite
        df["to_plot"] = df.apply(lambda x: 1 if x[e+"_percent"] > limite else x["to_plot"],axis=1)

    df = df.sort_index()
    for e in labels:
        c = e+"_percent"
        values = []
        names = []
        for index, row in df[df["to_plot"] == 1].iterrows():
            print(Limites[e])
            if(row[c] > Limites[e]):
                values.append(row[c])
            else:
                values.append(0)
                df[c].loc[index] = 0
            names.append(index)
        fig, ax = plt.subplots(figsize=(20, 9))
        plt.bar([e for e in range(len(values))],values,width=1,align='center')
        plt.xticks([e for e in range(len(values))],names,rotation="vertical")
        for i in range(len(values)):
            margin = max(values)/50
            if(df.loc[names[i]][c] > Limites[e]):
                plt.text(i, values[i]+margin, round(df.loc[names[i]][e],2), fontsize=10, ha='center')
        plt.margins(x=0, tight=True) ; fig.tight_layout() ; plt.subplots_adjust(top=0.95,bottom=0.15,left=0.05)
        plt.xlabel("features linguistics") ; plt.ylabel("weight (%)") ; plt.title("Signature "+e+" "+dico)
        ax.grid(axis="y")
        try :
            if(save != False and type(save) == str):
                plt.savefig(save+"Signature_"+e+"_"+dico+".png",)
        except FileNotFoundError:
            Path(save).mkdir(parents=True,exist_ok=True)
            if(save != False and type(save) == str):
                plt.savefig(save+"Signature_"+e+"_"+dico+".png",)
    if(plot):
        plt.show()


#Exemple of call to the main function
#compute_signature("",["NSR","SR"],save="/../../Graphs/SciTweetsGraph/FeaturesAnalysis/Signature/",plot=False)