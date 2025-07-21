import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

df = pd.read_excel("../../../SciTweets-Emo.xlsx")
Ekman = ['peur','colère','joie','surprise','tristesse','dégoût','neutre']
largeur_barre = 0.8
largeur_barre2 = 0.3
scientific_tweet = [0,0,0,0,0,0,0]
non_scientific_tweet = [0,0,0,0,0,0,0]

for index, row in df.iterrows():
    if(row['science_related']):
        scientific_tweet[row['emotions']-1] += 1
    else :
        non_scientific_tweet[row['emotions']-1] += 1
sommeSci = 0
sommeNonSci = 0
for i in scientific_tweet:
    sommeSci += i
for i in non_scientific_tweet:
    sommeNonSci += i

print("La somme de toutes les valeurs du tableau est "+str(sommeSci + sommeNonSci))

allDataset=[]

for i in range(len(scientific_tweet)):
    scientific_tweet[i] = scientific_tweet[i]*100/(sommeSci)
    non_scientific_tweet[i] = non_scientific_tweet[i]*100/(sommeNonSci)
    allDataset.append((scientific_tweet[i]+non_scientific_tweet[i])/2)

for i in range(len(scientific_tweet)):
    sum = scientific_tweet[i]+non_scientific_tweet[i]
    scientific_tweet[i] = scientific_tweet[i]*100/(sum)
    non_scientific_tweet[i] = non_scientific_tweet[i]*100/(sum)
    print(scientific_tweet[i]+non_scientific_tweet[i])

position1 = [i for i in range(0,14,2)]
position2 = [i + largeur_barre + 0.01 for i in position1]

fig = plt.figure(figsize=(15,8))
print(position1)
ax1 = plt.bar(position1, scientific_tweet, width = largeur_barre, color = "red")
ax2 = plt.bar(position1, non_scientific_tweet, width = largeur_barre, bottom = scientific_tweet, color = "blue")
ax3 = plt.bar(position2, allDataset, width=largeur_barre2, color="orange")
#plt.title('amout of tweets labeled with each emotion in each category',loc="left")
fig.legend([ax1,ax2,ax3],["scientific tweets","non_scientifc tweets","precentage of tweets labeled with the emotion in all the dataset"],loc="outside upper right")
plt.xticks(position1, Ekman)

#Objectif faire 3 diagrammes pour chaque type de tweets scientifiques

fig,axs = plt.subplots(2,2,figsize=(10,10))
fig.suptitle("Emotions distributions in scientific tweets")

emotions = [0.]*7
for index, row in df.loc[df["science_related"] == 1].iterrows():
    emotions[row["emotions"]-1] +=1
axs[0,0].pie(emotions,labels=Ekman)
axs[0,0].set_title("science related")

emotionsClaims = [0.]*7
for index, row in df.loc[df["scientific_claim"] == 1].iterrows():
    emotionsClaims[row["emotions"]-1] +=1
axs[0,1].pie(emotionsClaims,labels=Ekman)
axs[0,1].set_title("scientific claims")

emotionsReference = [0.]*7
for index, row in df.loc[df["scientific_reference"] == 1].iterrows():
    emotionsReference[row["emotions"]-1] +=1
axs[1,0].pie(emotionsReference,labels=Ekman)
axs[1,0].set_title("scientific references")

emotionsContext = [0.]*7
for index, row in df.loc[df["scientific_context"] == 1].iterrows():
    emotionsContext[row["emotions"]-1] +=1
axs[1,1].pie(emotionsContext,labels=Ekman)
axs[1,1].set_title("scientific context")

#---------------------------- non science related tweets ------------------------------

emotions = [0.]*7
for index, row in df.loc[df["science_related"] == 0].iterrows():
    emotions[row["emotions"]-1] +=1
plt.figure(figsize=(7,7))
plt.pie(emotions,labels=Ekman)
plt.title("Emotions distribution in non science related tweets")

#---------------------------- difference context and reference -------------------------
nbContext = df[((df["scientific_context"]==1))].shape[0]
for i in range(len(emotionsContext)):
    emotionsContext[i]=emotionsContext[i]/nbContext
nbRef = df[((df["scientific_reference"]==1))].shape[0]
for i in range(len(emotionsReference)):
    emotionsReference[i]=emotionsReference[i]/nbRef
nbClaims = df[((df["scientific_claim"]==1))].shape[0]
for i in range(len(emotionsClaims)):
    emotionsClaims[i]=emotionsClaims[i]/nbClaims
nbNonSci = df[((df["science_related"]==0))].shape[0]
for i in range(len(emotions)):
    emotions[i]=emotions[i]/nbNonSci
print("nombre de tweets labélisé context  : "+str(emotionsContext)+" , nombre de tweets labélisé référence : "+str(emotionsReference))
plt.figure(figsize=(8,6))
ax1, =plt.plot(emotionsContext,'o',color="green"); plt.plot(emotionsContext,'-',color="green")
ax2, =plt.plot(emotionsReference,'o',color="brown"); plt.plot(emotionsReference,'-',color="brown")
ax3, =plt.plot(emotionsClaims,'o',color="purple"); plt.plot(emotionsClaims,'-',color="purple")
ax4, =plt.plot(emotions,'o',color="blue"); plt.plot(emotions,'-',color="blue")
plt.legend([ax1,ax2,ax3,ax4],["context","references","claims","Non scientifiques"])
plt.xticks([i for i in range(7)],Ekman)
plt.title("emotions distributions in science_related sub-categories and non science_related")

#--------------------------- difference claims et moyenne ref context --------------------

emoAvg = [0]*7
for i in range(len(emotionsContext)):
    emoAvg[i]=(emotionsContext[i]+emotionsReference[i])/2
plt.figure(figsize=(10,6))
ax1, =plt.plot(emoAvg,'o',color="pink"); plt.plot(emoAvg,'-',color="pink")
ax3, =plt.plot(emotionsClaims,'o',color="purple"); plt.plot(emotionsClaims,'-',color="purple")
plt.legend([ax1,ax3],["Average Context and Reference","claims"]); plt.xticks([i for i in range(7)],Ekman)
plt.title("the difference in emotions distributions between scientific_claims nd the rest of the science_related class")

plt.show()
