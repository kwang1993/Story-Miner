
# coding: utf-8

# In[ ]:

#DATA_SET = "twitter"
DATA_SET = "mothering"
texts = []

if DATA_SET == "twitter":
    based_dir = '../data/Tweets/'
    file_input_name = 'sample.csv'
    file_input = based_dir + file_input_name      
    df = read_data(file_input,"twitter",",")#read the input sentences
    texts = df['main_tweet'].tolist()
    
elif DATA_SET == "mothering":
    based_dir = '../data/Vaccination/'
    file_input_name = 'sents.txt'
    #file_input_name = 'sent_cdb_child_exemption.txt'
    file_input = based_dir + file_input_name      
    df = read_data(file_input,"mothering","\n")#read the input sentences
    texts = df['text'].tolist()


# In[ ]:



