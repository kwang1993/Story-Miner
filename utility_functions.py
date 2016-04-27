
# coding: utf-8

# In[ ]:

#from collections import Counter
from collections import Counter

def read_data(dataset="twitter", delim=","):
    if dataset == "twitter":
        based_dir = '../data/Tweets/'
        file_input_name = 'sample.csv'
        file_input = based_dir + file_input_name        
        ff = open(file_input)
        h = ff.readline()
        header_orig = h.split(delim)
        df = pd.read_csv(file_input,delimiter=delim, header=0)#names=header_orig)
        #print df.tweet_id[0:10]
        df['tweet_posted_time'] = df['tweet_posted_time'].apply(lambda x: datetime.strptime(x.split('.')[0],                                                                                             '%Y-%m-%dT%H:%M:%S'))
        selected_columns = ['tweet_posted_time', 'tweet_text', 'main_tweet', 'ollie_conf',                 'ollie_arg1', 'ollie_rel', 'ollie_arg2', 'clean_tweet_polarity','clean_tweet_subjectivity']
        df_selected = df[[i for i in df.columns if i in selected_columns]]
        #print "df_selected values - 1"
        #df_selected.values_counts()
        #print len(df_selected.index)
        df_selected = df_selected.dropna(how = 'any')
        print "Number of instances: "    
        print len(df_selected.index)
        #print " selected dataframe - index 0 : ", df_selected.iloc[0]
        return df_selected
    if dataset == "mothering":
        based_dir = '../data/Vaccination/'
        file_input_name = 'sent_cdb_child_exemption.txt'
        file_input = based_dir + file_input_name    
        ff = open(file_input)
        delim='\n'
        df = pd.read_csv(file_input,delimiter=delim,header=0)        
        return df

def plot_argument_graph(g):
    A = nx.nx_agraph.to_agraph(g)
    A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    d = draw(g, show='ipynb')
    display(d)    
    
def plot_dep(g,title):
    '''
    This function takes a DIRECTED graph as input, and plot it inline in Ipython.
    '''
    #set figure size
    '''
    plt.figure(figsize=(14,8))
    #set style of the graph
    pos = graphviz_layout(g,prog='dot')

    # 
    node_labels = nx.get_node_attributes(g, "id")
    nx.draw_networkx_labels(g, pos, labels = node_labels, font_size=11)
    edge_labels_tupels = nx.get_edge_attributes(g, "rel")
    #print edge_labels_tupels
    #edge_labels = [(e[0][0],e[0][1],e[1].value()) for e in edge_labels_tupels]
    edge_labels = edge_labels_tupels
    #edge_labels = edge_labels_dict.values()
    #print edge_labels
    nx.draw_networkx_edge_labels(g, pos, labels = edge_labels)
    nx.draw_networkx(g,pos=pos,  arrows=True, with_labels=False, node_size=1500, alpha=0.3, node_shape = 's') 
    
    #nx.nx_pylab.  
    plt.title(title)
    plt.savefig('Dep_tree.png')
    plt.show()
    '''
    A = nx.nx_agraph.to_agraph(g)
    A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    A.draw('test.png')
    
    d = draw(g, show='ipynb')
    display(d)
    
def print_relations(rels):
    if len(rels) < 1:
        print "No extraction."
        return
    for ind,r in enumerate(rels):
        print "> Extraction Number: ",ind+1, " - ", "Pattern: ", r["pattern"],"relation : ( ", r["arg1"], ", ", r["rel"], ", ", r["arg2"] ," )"
    print " -------------------------------- \n"

def get_rels_str(rels):
    if len(rels) < 1:
        return []
    rels_str = []
    for r in rels:
        r_str = "( " + r["arg1"] + ", " + r["rel"] + ", " + r["arg2"] + " )"
        rels_str.append(r_str)
    return rels_str
    
def saveToFile_rows(outputLoc, inputList, delim):
    with open(outputLoc,"wb") as f:
        writer = csv.writer(f,delimiter=delim)
        writer.writerows(inputList)   
        
def print_top_relations(all_rels,top_num=-1):
    cnt = Counter()
    for r in all_rels:
        cnt[r] += 1
    if top_num == -1: # means print all
        print "Frequent relations:"
        for letter,count in cnt.most_common():
            print letter, ": ", count
    else:
        print "top ", top_num, " frequent relations:"
        for letter,count in cnt.most_common(top_num):
            print letter, ": ", count        


# In[ ]:

get_ipython().run_cell_magic(u'javascript', u'', u"var add_edit_shortcuts = {\n    'shift-enter' : {\n                help : 'run cell, select next codecell',\n                help_index : 'bb',\n                handler : function (event) {\n                IPython.notebook.execute_cell_and_select_below();\n                // find next CodeCell and go into edit mode if possible, else stay in next cell\n                var i;\n                for (i = IPython.notebook.get_selected_index(); i < IPython.notebook.ncells() ;i++) {\n                var cell = IPython.notebook.get_cell(i);\n                if (cell instanceof IPython.CodeCell) {\n                    IPython.notebook.select(i);\n                    IPython.notebook.edit_mode();\n                    break;\n                }\n            }\n            return false;\n        }\n    },\n};\n\nIPython.keyboard_manager.edit_shortcuts.add_shortcuts(add_edit_shortcuts); ")


# In[ ]:



