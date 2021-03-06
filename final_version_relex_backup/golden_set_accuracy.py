from init import *
import csv
import pandas as pd

import main_functions
#import parameters
import utility_functions
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def load_data(path_to_file):
    data = []
    with open(path_to_file, 'rb') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for ind, row in enumerate(csv_reader):
            if ind == 0 :
                header = row
                continue
            data.append(row)
    
    print header
    print data[0]
    return data, header

def extract_relations(sent):
    #print type(sent)
    #print sent
    annotator = Annotator()
    try:
        t_annotated = annotator.getAnnotations(sent, dep_parse=True)
    except:
        print "Error in sentence annotation"
        return
    try:
        g_dir = create_dep_graph(t_annotated)
        if g_dir is None:
            print "No extraction found"
            return
        #if SHOW_DP_PLOTS:
        #    plot_dep(g_dir,t)
        g_undir = g_dir.to_undirected()
    except:
        print "Unexpected error while extracting relations:", sys.exc_info()[0]
        return
    rels_pure, rels_simp = get_relations(g_dir, t_annotated, option="SVO")
    rels = rels_pure#rels_simp
    return get_rels_str(rels)




def evaluate_golden_set(df , sent_label):
    cols = list(df.columns) + ["relEx_results"]
    df_res = pd.DataFrame(columns = cols)
    for ind, row in df.iterrows():
        #if ind >0 : 
        #    break
        sent = row[sent_label]
        print sent
        rels = extract_relations(sent)
        print "-------Start------"
        print rels
        print " ------END------"
        df_res.loc[len(df_res)] = row.tolist() + [rels]
    return df_res

def main():
    path_to_input_file = "../../data/Vaccination/golden_set.csv"
    path_to_output_file = "../../data/Vaccination/golden_set_with_extractions.csv"
    data, header = load_data(path_to_input_file)
    df = pd.DataFrame(data, columns = header )        
    df_res = evaluate_golden_set(df.copy(), sent_label="Text")
    print df_res.iloc[10]
    df_res.to_csv(path_to_output_file, sep=',')
    print "Done"
            

if __name__ == "__main__":
    main()


