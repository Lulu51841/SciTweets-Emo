import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df = pd.read_excel("../../Data/Topics/topicBigCat.xlsx")

Ekman = ['fear','anger','joy','surprise','sadness','disgust','neutral']

counts = df.value_counts("topic")
print(counts)
plotted_topic = [] ; values = []
for index, value in counts.items():
    if value > 40 and index != -1:
        plotted_topic.append(index)
        values.append(value)

counts_sci = df[df["science_related"] == 1].value_counts("topic")
counts_non_sci = df[df["science_related"] == 0].value_counts("topic")
values_sci = [] ; values_non_sci = []
for i in plotted_topic:
    values_sci.append(counts_sci[i])
    values_non_sci.append(counts_non_sci[i])

nb_science = df["science_related"].sum()
nb_normal = df.shape[0]-nb_science
print(nb_normal)
nb_no_cat = 0
nb_no_cat_sci = 0
for i in range(len(plotted_topic)):
    nb_no_cat+=values_non_sci[i]
    nb_no_cat_sci+=values_sci[i]

print("Pourcentages des tweets de chaque catégories qui sont dans aucun des 4 topics, science_related :  "+str(nb_no_cat_sci/nb_science)+" , non science_related : "+str(nb_no_cat/nb_normal))

#for i in range(len(plotted_topic)):
#    values_sci[i] = values_sci[i]/nb_science
#    values_non_sci[i] = values_non_sci[i]/nb_normal
#    sum = values_sci[i] + values_non_sci[i]
#    values_sci[i] = values_sci[i]/sum * values[i]
#    values_non_sci[i] = values_non_sci[i]/sum * values[i]
#    print((values_non_sci[i]+values_sci[i])/values[i])

print(plotted_topic)
topics_names = ["sport","politic","health","work related","technologies","finance","climat and biodiversity","ethnic and religious conflict","love&sex","meta-science",
"lgbtq","religion","art"]

labels = [topics_names[e] for e in plotted_topic]
position = [e for e in range(len(plotted_topic))]
largeur_barre = 0.8
fig = plt.figure(figsize=(6,6))
ax1 = plt.bar(position, values_sci, width = largeur_barre, color = "red")
ax2 = plt.bar(position, values_non_sci, width = largeur_barre, bottom = values_sci, color = "blue")
fig.legend([ax1,ax2],["science related tweets","non science_related tweets"],draggable=True)
#plt.title('most discussed topic in the SciTweets dataset')
plt.xticks(position, labels)

# Add numbers on the top of each bar
for i in range(len(plotted_topic)):
    plt.text(position[i], values[i] + 2, values[i], fontsize=10, ha='center')

listEmo = []
for i in range(len(Ekman)):
    listEmo.append([])
    for t in plotted_topic:
        #print(df[(df["topic"] == t) & (df["emotions"] == i)].shape[0])
        listEmo[i].append(df[(df["topic"] == t) & (df["emotions"] == i+1)].shape[0])

cpt = 0
for i in listEmo[0]:
    cpt+=i
print(listEmo)

fig = plt.figure(figsize=(6,6))
largeur_barre = 0.8 ; axs = [plt.bar(position, listEmo[0], width=largeur_barre)] ; sumTab = np.array(listEmo[0])
for i in range(1,len(Ekman)):
    print("sumTab = "+str(sumTab[0])+" ; values = "+str((np.array(listEmo[i]) + sumTab)[0]))
    axs.append(plt.bar(position, np.array(listEmo[i]), bottom=sumTab, width=largeur_barre)) ; sumTab += np.array(listEmo[i])
fig.legend(axs,Ekman,draggable=True)
#plt.title("emotions in the most discussed topics")
plt.xticks(position, labels)


plt.show()