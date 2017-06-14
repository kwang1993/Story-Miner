import os
import sys
sys.path.insert(0, './base_codes')
sys.path.insert(0, './data_specific_codes')
sys.path.insert(0, './utility_codes')

from base_codes.RE_init import *
from base_codes.main_functions import *
from base_codes.utility_functions import *

'''
PARAMETERS
'''
SEPARATE_SENT = True
CLEAN_SENTENCES = True
SHOW_DP_PLOTS = False
SHOW_REL_EXTRACTIONS = False
NODE_SELECTION = False
MAX_ITERATION = -1 #-1 -> to try all
SAVE_GEFX = False
SAVE_G_JSON = False
SAVE_PAIRWISE_RELS = False
SAVE_ALL_RELS = False 
SET_INOUT_LOC_FROM_PYTHON_ARGS = True 
SHOW_ARGUMENT_GRAPH = False
EXTRACT_NESTED_PREPOSITIONS_RELS = True 
DATA_SET = "goodreads"
INPUT_DELIMITER = "\n"
SAVE_ANNOTATIONS_TO_FILE = True
LOAD_ANNOTATIONS = False 
KEEP_ORDER_OF_EXTRACTIONS = True 




data_dir = "../../data/"
texts = []

if SET_INOUT_LOC_FROM_PYTHON_ARGS:
    file_input_arg = str(sys.argv[1])
    output_dir_arg = str(sys.argv[2])
    input_fname = os.path.basename(file_input_arg)
    input_fname = str(input_fname.split(".")[0])
    output_prefix = output_dir_arg + input_fname
else:
    if LOAD_ANNOTATIONS:
        input_fname = 'sents_1'
        file_input_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'+input_fname+'.csv'
        output_dir_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'
    else:
        input_fname = 'sents_1'
        file_input_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'+input_fname+'.csv'
        output_dir_arg = '/Users/behnam/Desktop/Behnam_Files/vwani_text_mining/RE_Behnam/data/Tweets/'
        
    


#file_input = get_file_input(DATA_SET)


all_rels_str = []
all_rels = []
output = []

start_time = time.time()

all_rels_str, all_rels, output = text_corpus_to_rels(file_input_arg,
                                                     DATA_SET,
                                                     INPUT_DELIMITER,
                                                     input_fname,
                                                     output_dir_arg,
                                                     MAX_ITERATION,
                                                     CLEAN_SENTENCES,
                                                     SEPARATE_SENT,
                                                     SHOW_DP_PLOTS,
                                                     SHOW_REL_EXTRACTIONS,
                                                     SAVE_ALL_RELS,
                                                     EXTRACT_NESTED_PREPOSITIONS_RELS,
                                                     SAVE_ANNOTATIONS_TO_FILE,
                                                     LOAD_ANNOTATIONS,
                                                     KEEP_ORDER_OF_EXTRACTIONS
                                                    )            
end_time = time.time()
print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
print "***************STATISTICS***************"
#print "Total number of input records (posts): ", len(texts)
print "Total number of extracted relations: ", len(all_rels_str)
print_top_relations(all_rels_str,output_dir_arg+input_fname+'_top_rels.txt',top_num=-1) 
df_rels = pd.DataFrame(all_rels)
df_output = pd.DataFrame(output)

#print df_rels
'''
rels_to_network(df_rels,
                input_fname,
                output_dir_arg,
                MAX_ITERATION,
                NODE_SELECTION,
                DATA_SET,
                SAVE_GEFX,
                SAVE_PAIRWISE_RELS,
                SHOW_ARGUMENT_GRAPH,
                SAVE_G_JSON
               )
'''
#if __name__ == "__main__":
#    main(sys.argv[1:])
#'''

