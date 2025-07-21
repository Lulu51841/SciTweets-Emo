import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

Ekman = ['peur','colère','joie','surprise','tristesse','dégoût','neutre']

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


df = pd.read_csv("resultSEANCE/resultsEmo.csv")

df = df.T

df.columns = Ekman
df = df.iloc[2:]

plt.figure(figsize=(10,7))
axes = []
for i in df.columns:
    df = df.sort_values(i,ascending=False)
    axes.append(plt.plot(list(df[i]),'-')[0])

plt.legend(axes,Ekman)





#for i in range(len(df.columns)):
#    df = df.sort_values(df.columns[i],ascending=False)
#    limite = takeFirstPercent(df,df.columns[i],0.15)
#    ternary = to_ternary(i)
#    print(ternary)
#    axs[ternary[0],ternary[1]].pie(df[df.columns[i]].iloc[:limite+1],labels=df.iloc[:limite+1].index)
#    axs[ternary[0],ternary[1]].set_title(df.columns[i])

Limites = {}
df["to_plot"] = 0
for e in Ekman:
    df = compute_percents(df,e)
    index,w,limite = getLastIn(df,e,0.50)
    print(limite)
    Limites[e] = limite
    df["to_plot"] = df.apply(lambda x: 1 if x[e+"_percent"] > limite else x["to_plot"],axis=1)

df = df.sort_index()

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Quan_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Quan_Gi')
plt.xticks(position, Ekman)

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Sv_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Sv_Gi')
plt.xticks(position, Ekman)

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Power_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Power_Gi')
plt.xticks(position, Ekman)

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Comform_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Comform_Gi')
plt.xticks(position, Ekman)

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Socrel_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Socrel_Gi')
plt.xticks(position, Ekman)

df1 = df[['peur_percent','colère_percent','joie_percent','surprise_percent','tristesse_percent','dégoût_percent','neutre_percent']].loc["'Virtue_GI'"]

position = [e for e in range(7)]
largeur_barre = 0.8
fig = plt.figure(figsize=(10,8))
ax1 = plt.bar(position, df1, width = largeur_barre)
plt.title('Percentages of the weight of each emotion for the feature Virtue_Gi')
plt.xticks(position, Ekman)

plt.show()
exit()
print(df.head())
for e in Ekman:
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
    plt.xlabel("features linguistics") ; plt.ylabel("weight (%)") ; plt.title("Signature "+e+" GI")
    ax.grid(axis="y")
    plt.savefig("../mesGraphs/signature_Ling/GI/Signature_"+e+"_GI.png",)
plt.close()
#Conclusion sur le graph des features linguistiques par emotions
#Konstantin a dit : pas intéressant, il a pas tort