import os
import sys
sys.path.insert(0, './base-codes')
sys.path.insert(0, './data-specific-codes')
sys.path.insert(0, './utility-codes')

from init import *
from main_functions import *
from utility_functions import *

'''
PARAMETERS
'''
SEPARATE_SENT = False 
SHOW_DP_PLOTS = False
SHOW_REL_EXTRACTIONS = False
NODE_SELECTION = True
MAX_ITERATION = 4#-1 #-1 -> to try all
SAVE_GEFX = True
SAVE_PAIRWISE_RELS = True
SAVE_ALL_RELS = False 
CLEAN_SENTENCES = False
SET_INOUT_LOC_FROM_PYTHON_ARGS = False
SHOW_ARGUMENT_GRAPH = True
EXTRACT_NESTED_PREPOSITIONS_RELS = False
DATA_SET = "sentence_only"



data_dir = "../../data/"
texts = []

if SET_INOUT_LOC_FROM_PYTHON_ARGS:
    file_input_arg = str(sys.argv[1])
    output_dir_arg = str(sys.argv[2])
    input_fname = os.path.basename(file_input_arg)
    input_fname = str(input_fname.split(".")[0])
    output_prefix = output_dir_arg + input_fname
else:
    input_fname = 'tweets_textOnly'
    file_input_arg = data_dir + 'Tweets/' + 'tweets_textOnly_sample.txt'
    output_dir_arg = data_dir + 'Tweets/'
    


#file_input = get_file_input(DATA_SET)
df = read_data(file_input_arg, DATA_SET, "\n")
texts = df['text'].tolist()


all_rels_str = []
all_rels = []
output = []

start_time = time.time()

all_rels_str, all_rels, output = text_corpus_to_rels(texts,
                                                     input_fname,
                                                     output_dir_arg,
                                                     MAX_ITERATION,
                                                     CLEAN_SENTENCES,
                                                     SEPARATE_SENT,
                                                     SHOW_DP_PLOTS,
                                                     SHOW_REL_EXTRACTIONS,
                                                     SAVE_ALL_RELS,
                                                     EXTRACT_NESTED_PREPOSITIONS_RELS
                                                    )            
end_time = time.time()
print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
print "***************STATISTICS***************"
print "Total number of input records (posts): ", len(texts)
print "Total number of extracted relations: ", len(all_rels_str)
print_top_relations(all_rels_str,top_num=-1) 
df_rels = pd.DataFrame(all_rels)
df_output = pd.DataFrame(output)

rels_to_network(df_rels,
                input_fname,
                output_dir_arg,
                MAX_ITERATION,
                NODE_SELECTION,
                DATA_SET,
                SAVE_GEFX,
                SAVE_PAIRWISE_RELS,
                SHOW_ARGUMENT_GRAPH
               )

#if __name__ == "__main__":
#    main(sys.argv[1:])
#'''

