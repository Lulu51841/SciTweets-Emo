import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df = pd.read_excel("Data/BerTopic_step1.xlsx")

topic_to_browse = 1

dfTopic = df[(df["topic"] == topic_to_browse)]


print(dfTopic.head())

dfTopic.to_excel('Data/browse/step2/browse_topic'+str(topic_to_browse)+'.xlsx',index=False)