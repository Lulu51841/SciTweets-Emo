import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df_SR = pd.read_excel("../../../SciTweets-Emo.xlsx")

nb_SR = df_SR[df_SR["science_related"] == 1].shape[0]

print(nb_SR)

df_topics = pd.read_excel("../../Data/Topics/BerTopic_step1.xlsx")

topics_names = ["sport","politic","health","work related","technologies","finance","epidemic disease","infections","climat and biodiversity",
"cancer","ethnic and religious conflict","neurosciences","love&sex","meta-science","lgbtq","mental health","religion","music","movie"]

climat = df_topics[df_topics["topic"] == 8].shape[0]

covid = df_topics[df_topics["topic"] == 6].shape[0]

labels = ["science related","climat and biodiversity","epidemic diseases"]
position = [e for e in range(3)]
largeur_barre = 0.8
fig = plt.figure(figsize=(6,6))
plt.bar(position, [nb_SR,climat,covid], width = largeur_barre)
plt.xticks(position, labels)
plt.show()