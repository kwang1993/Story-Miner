
# coding: utf-8

# In[ ]:

#DATA_SET = "twitter"
DATA_SET = "mothering"
texts = []

if DATA_SET == "twitter":
    df = read_data("twitter",",")#read the input sentences
    texts = df['main_tweet'].tolist()
    
elif DATA_SET == "mothering":
    df = read_data("mothering","\n")#read the input sentences
    texts = df['text'].tolist()


# In[ ]:



