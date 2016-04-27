
# coding: utf-8

# In[6]:

def create_node_attributes(n, annotation):
    '''
    This function takes a node and 
    '''
    # ROOT does not appear in the tree
    n_att = {}
    if n == "ROOT-0":
        n_word = "ROOT"
        n_att["word"] = n_word
        n_att["id"] = n
        return n_att
    
    # extract attributes
    n_splitted = n.split('-')
    n_word, n_ind = n.split('-')[0], n.split('-')[1]
    try:
        n_ind = int(n_ind) - 1 # make it 0 base - ROOT becomes "-1"
    except:
        print "Tokenizer failed during parsing, Ex. there might be a dash in the sentence!"
        return None
    n_pos = annotation['pos'][n_ind][1]
    
    n_att["word"] = n_word
    n_att["ind"] = n_ind
    n_att["pos"] = n_pos
    n_att["id"] = n
    
    return n_att
        
def create_dep_graph(annotation):
    dep_parse = annotation['dep_parse']
    if dep_parse == '':
        return None
    dp_list = dep_parse.split('\n')
    #print dp_list
    pattern = re.compile(r'.+?\((.+?), (.+?)\)')    
    #g = nx.Graph()
    g_dir = nx.DiGraph()
    for dep in dp_list:
        m = pattern.search(dep)
        n1 = m.group(1)#.split('-')[0]
        n2 = m.group(2)#.split('-')[0]
        n1_att = create_node_attributes(n1, annotation)
        n2_att = create_node_attributes(n2, annotation)
        if n1_att is None or n2_att is None:
            return None
        g_dir.add_node(n1, n1_att)
        g_dir.add_node(n2, n2_att)
        e_rel = dep[:dep.find("(")]
        #edges.append(e)
        g_dir.add_edge(n1, n2, {'rel' : e_rel}, label = e_rel)
    return g_dir

def get_simp_rel(rel, option = "SVO"):
    # add options later
    '''
    Lower case, Strip
    '''
    arg1 = rel['arg1'].lower().strip()
    arg2 = rel['arg2'].lower().strip()
    r = rel['rel'].lower().strip()

    '''
    Mapping:
    (I,You,We -> Parents)
    '''    
    parent_list = ["i","you","we","your","us","they"]
    if arg1 in parent_list:
        arg1 = "parent"
    if arg2 in parent_list:
        arg2 = "parent"
        
    child_list = ["children","kid","kids","child","son","daughter"]
    if arg1 in child_list:
        arg1 = "child"
    if arg2 in child_list:
        arg2 = "child"    
    '''
    Stemming
    '''
    stemmer = SnowballStemmer("english")
    arg1 = stemmer.stem(arg1) 
    arg2 = stemmer.stem(arg2)
    r = stemmer.stem(r)
    
    rel_simp = rel
    rel_simp['arg1'] = arg1
    rel_simp['arg2'] = arg2
    rel_simp['rel'] = r
    return rel_simp


    

def get_relations(g_dir, annotation, option="SVO"):
    relations = []
    '''
    Simplified relations:
    meaning that we only keep head words, do stemming, map words to their actual actor ( I,we,you -> parents)
    '''
    relations_simp = [] 
    if option == "SVO":
        t_verbs = annotation['verbs']
        for v in t_verbs:
            v_id = v+"-"+str(annotation['words'].index(v)+1) 
            try:
                g_dir_v = g_dir[v_id] #adjacency of v_id
            except:
                print v_id, " does not appeared as a separate node in parsing tree."
                continue
            nsubj_list = []
            dobj_list = []
            for word_id, e in g_dir_v.iteritems():
                if e["rel"] == "nsubj":
                    nsubj_list.append(word_id)
                if e["rel"] == "dobj":
                    dobj_list.append(word_id)
            if len(nsubj_list) > 0 and len(dobj_list) > 0:
                for s in nsubj_list:
                    for o in dobj_list:
                        rel = {}
                        rel["rel"] = v
                        rel["arg1"] = s.split("-")[0]
                        rel["arg2"] = o.split("-")[0]
                        rel["pattern"] = "(nsubj, verb, dobj)"
                        relations.append(rel)
                        rel_simp = get_simp_rel(rel,option)
                        relations_simp.append(rel_simp)
    return relations, relations_simp

def create_argument_graph(df, source, target, edge_attr=None, graph_type="directed"):
    ''' Return a graph from Pandas DataFrame.
    Modified version of "from_pandas_dataframe" function.
    '''
    if graph_type == "undirected":
        g = nx.Graph()
    elif graph_type == "directed":
        g = nx.DiGraph()
    else:
        g = nx.MultiGraph()
    
    src_i = df.columns.get_loc(source)
    tar_i = df.columns.get_loc(target)
    label_i = df.columns.get_loc(edge_attr)
    if edge_attr:
        # If all additional columns requested, build up a list of tuples
        # [(name, index),...]
        if edge_attr is True:
            # Create a list of all columns indices, ignore nodes
            edge_i = []
            for i, col in enumerate(df.columns):
                if col is not source and col is not target:
                    edge_i.append((col, i))
        # If a list or tuple of name is requested
        elif isinstance(edge_attr, (list, tuple)):
            edge_i = [(i, df.columns.get_loc(i)) for i in edge_attr]
        # If a string or int is passed
        else:
            edge_i = [(edge_attr, df.columns.get_loc(edge_attr)),]

        # Iteration on values returns the rows as Numpy arrays
        for row in df.values:
            g.add_edge(row[src_i], row[tar_i], label = row[label_i])#{i:row[j] for i, j in edge_i},label=row[label_i])
    
    # If no column names are given, then just return the edges.
    else:
        for row in df.values:
            g.add_edge(row[src_i], row[tar_i])

    return g

def create_argument_multiGraph(df, source, target):
    g = nx.MultiGraph()
    print df
    nodes = set()
    nodes = list(nodes.union(df[source],df[target]))
    for n in nodes:
        g.add_node(n)
        ''' Get dataframe in which n is the source'''
        df_n = df[df[source] == n]
        
        g.add_edge(n,)
    return nodes


# In[ ]:



