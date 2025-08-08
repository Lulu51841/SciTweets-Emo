import matplotlib.pyplot as plt

largeur_barre = 0.8
largeur_barre2 = 0.3
Ekman = ['fear','anger','joy','surprise','sadness','disgust']

import pandas as pd
import numpy as np

df = pd.read_excel("../../Data/CancerEmo/CancerEmo_Sci.xlsx")

scientific_tweet = [0,0,0,0,0,0]
non_scientific_tweet = [0,0,0,0,0,0]

for index, row in df.iterrows():
    #print("on est daccord ça passe ?????")
    emo = list(map(int,row["emotions"][1:-1].split(",")))
    if(row["science_related"] == 1):
        #print("Ui ???")
        for i in range(len(scientific_tweet)):
            if emo[i] == 1:
                scientific_tweet[i]+=1
    else:
        for i in range(len(non_scientific_tweet)):
            if emo[i] == 1:
                non_scientific_tweet[i]+=1

print(scientific_tweet)
print(non_scientific_tweet)

sommeSci = df["science_related"].sum()
sommeNonSci = df.shape[0] - df["science_related"].sum()
emotions = non_scientific_tweet/sommeNonSci

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

print(scientific_tweet)
print(non_scientific_tweet)

#----------------------------------- graph -------------------------------------

position1 = [i for i in range(0,12,2)]
position2 = [i + largeur_barre + 0.01 for i in position1]

fig = plt.figure(figsize=(15,8))
ax1 = plt.bar(position1, scientific_tweet, width = largeur_barre, color = "red")
ax2 = plt.bar(position1, non_scientific_tweet, width = largeur_barre, bottom = scientific_tweet, color = "blue")
ax3 = plt.bar(position2, allDataset, width=largeur_barre2, color="orange")
#plt.title('amout of tweets labeled with each emotion in each category',loc="left")
fig.legend([ax1,ax2,ax3],["scientific tweets","non_scientifc tweets","precentage of tweets labeled with the emotion in all the dataset"],loc="outside upper center",fontsize="large")
plt.xticks(position1, Ekman)

#----------------------------------- second graph ------------------------------

emotionsClaims = [0]*6
emotionsContext = [0]*6
emotionsReference = [0]*6

for index, row in df.iterrows():
    #print("on est daccord ça passe ?????")
    emo = list(map(int,row["emotions"][1:-1].split(",")))
    if(row["scientific_claim"] == 1):
        #print("Ui ???")
        for i in range(len(emotionsClaims)):
            if emo[i] == 1:
                emotionsClaims[i]+=1
    if(row["scientific_context"] == 1):
        for i in range(len(emotionsContext)):
            if emo[i] == 1:
                emotionsContext[i]+=1
    if(row["scientific_reference"] == 1):
        for i in range(len(emotionsReference)):
            if emo[i] == 1:
                emotionsReference[i]+=1

nbClaims = df["scientific_claim"].sum()
for i in range(len(emotionsClaims)):
    emotionsClaims[i]=emotionsClaims[i]/nbClaims
nbContext = df["scientific_context"].sum()
for i in range(len(emotionsContext)):
    emotionsContext[i]=emotionsContext[i]/nbContext
nbRef = df["scientific_reference"].sum()
for i in range(len(emotionsReference)):
    emotionsReference[i]=emotionsReference[i]/nbRef


emoAvg = [0]*6
for i in range(len(emotionsContext)):
    emoAvg[i]=(emotionsContext[i]+emotionsReference[i])/2
plt.figure(figsize=(10,6))
ax1, =plt.plot(emoAvg,'o',color="pink")
plt.plot(emoAvg,'-',color="pink")
ax3, =plt.plot(emotionsClaims,'o',color="purple")
plt.plot(emotionsClaims,'-',color="purple")
plt.legend([ax1,ax3],["Average Context and Reference","claims"])
plt.xticks([i for i in range(6)],Ekman)
plt.title("the difference in emotions distributions between scientific_claims nd the rest of the science_related class")

#------------------------- third graph -------------------------------------

plt.figure(figsize=(8,6))
ax1, =plt.plot(emotionsContext,'o',color="green")
plt.plot(emotionsContext,'-',color="green")
ax2, =plt.plot(emotionsReference,'o',color="brown")
plt.plot(emotionsReference,'-',color="brown")
ax3, =plt.plot(emotionsClaims,'o',color="purple")
plt.plot(emotionsClaims,'-',color="purple")
ax4, =plt.plot(emotions,'o',color="blue")
plt.plot(emotions,'-',color="blue")
plt.legend([ax1,ax2,ax3,ax4],["context","references","claims","Non scientifiques"])
plt.xticks([i for i in range(6)],Ekman)
plt.title("emotions distributions in science_related sub-categories and non science_related")

plt.show()