import pandas as pd
import numpy as np
print(np.version.version)
df = pd.read_excel("../../../SciTweets-Emo.xlsx")


with open('tweets_sci.txt','w') as f:
    for index, value in df[df["science_related"] == 1]["text"].items():
        f.write(value+"\n")

with open('tweets_non_sci.txt','w') as f:
    for index, value in df[df["science_related"] == 0]["text"].items():
        f.write(value+"\n")


#for i in range(1,8):
#    with open('tweets_emo_'+str(i)+'.txt','w') as f:
#        for index, value in df[df["emotions"] == i]["text"].items():
#            f.write(value+"\n")

#for i in range(1,8):
#    with open('tweets_sci_'+str(i)+'.txt','w') as f:
#        for index, value in df[(df["emotions"] == i) & (df["science_related"] == 1)]["text"].items():
#            f.write(value+"\n")
#    with open('tweets_non_sci'+str(i)+'.txt','w') as f:
#        for index, value in df[(df["emotions"] == i) & (df["science_related"] == 0)]["text"].items():
#            f.write(value+"\n")
#
#with open('tweets_claims.txt','w') as f:
#    for index, value in df[df["scientific_claim"] == 1]["text"].items():
#        f.write(value+"\n")
#
#with open('tweets_context.txt','w') as f:
#    for index, value in df[df["scientific_context"] == 1]["text"].items():
#        f.write(value+"\n")
#
#with open('tweets_ref.txt','w') as f:
#    for index, value in df[df["scientific_reference"] == 1]["text"].items():
#        f.write(value+"\n")