from utils import emotionsOnTweetsCaracteristic,find_hashtags
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


def create_topics_from_words(row):
    print(row)
    if("gender" in str(row["words"])):
        row["topic"]=14
        row["words"]=""
    if("genders" in str(row["words"])):
        print("yep")
        row["topic"]=14
        row["words"]=""
    if("mentale" in str(row["words"])):
        row["topic"]=15
        row["words"]=""
    if("religion" in str(row["words"])):
        row["topic"]=16
        row["words"]=""
    if("music" in str(row["words"])):
        row["topic"]=17
        row["words"]=""
    if("movie" in str(row["words"])):
        row["topic"]=18
        row["words"]=""
    return row

#------------------------------------ creating first version of compiled dataset --------------------------------------------

def create_final_df():
    topics_df = [pd.read_excel('../../Data/browse/browse_topic'+str(-1)+'.xlsx')]
    df = topics_df[0]
    print(df.shape)
    for i in range(14):
        topics_df.append(pd.read_excel('Data/browse/browse_topic'+str(i)+'.xlsx'))
        df = pd.concat([df,topics_df[i+1]])
        print('File : Data/browse/browse_topic'+str(i)+'.xlsx , size of df : '+str(df.shape))

    print(df.columns)

    df_final = df.apply(lambda x: create_topics_from_words(x),axis=1)

    df_final.to_excel('../../Data/BerTopic_step1.xlsx',index=False)
    return df_final


#----------------------------------- playing with the unlabeled data ---------------------------------------------------
def handle_sports(df):

    def mapping(x):
        if "sportive" in str(x["words"]):
            x["topic"]=0
        return x

    def extract_subDf(x):
        if (("love" in str(x["words"])) or ("sex" in str(x["words"]))):
            print(x)
            return x


    df_final = df.apply(lambda x: mapping(x),axis=1)

    df_final.to_excel('../../Data/BerTopic_step1.xlsx',index=False)

    df_love = df_final[(df_final["words"] == "love") | (df_final["words"] == "sex")]
    
    df_love.to_excel('../../Data/browse/topic_love&sex.xlsx',index=False)

    return df_final


def create_loveNsex_cat(df):

    def map(x):
        if "love" in str(x["words"]) or "sex" in str(x["words"]):
            x["topic"]=19
        return x
    
    if(type(df) is str):
        df = pd.read_excel(df)
    
    df_final = df.apply(lambda x: map(x),axis=1)
    df_final.to_excel('../../Data/BerTopic_step1.xlsx',index=False)

    return df_final

def correct_sante_cat(df):

    def map(x):
        if "santé" in str(x["words"]):
            x["topic"]=2
        if x["topic"] == 12 :
            x["topic"] = 2
        if x ["topic"] == 19 :
            x["topic"] = 12
        return x
    
    if(type(df) is str):
        df = pd.read_excel(df)
    
    df_final = df.apply(lambda x: map(x),axis=1)
    df_final.to_excel('../../Data/BerTopic_step1.xlsx',index=False)

#------------------------------------------------ counts differents labels ---------------------------------------------

def get_count_words(df):

    if(type(df) is str):
        df = pd.read_excel(df)
    
    print(df[df["topic"] == -1]["words"].value_counts())

def get_count_topics(df):

    if(type(df) is str):
        df = pd.read_excel(df)
    
    print(df["topic"].value_counts())


#--------------------------- concatenate emotion df, science_related df and topic df -----------------------------------

def concat_df(df1,df2):
    if(type(df1) is str):
        df1 = pd.read_excel(df1)
    
    if(type(df2) is str):
        df2 = pd.read_excel(df2)
    
    df1["topic"] = df2["topic"]
    df1["words"] = df2["words"]
    df1.to_excel('../../Data/annotation_topic.xlsx',index=False)
    return df1

concat_df("../../../SciTweets-Emo.xlsx","../../Data/BerTopic_step1.xlsx")