from RE_init import *
import string
from collections import Counter
#from collections import Counter
#import pandas as pd

def read_data(file_input,dataset="twitter",delim=",", LOAD_ANNOTATIONS=False):
    print file_input
    if dataset == "twitter-v0":      
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
    
        
    if dataset == "mothering" or dataset == "sentence_only" or dataset == "goodreads" or "goodreads" in dataset: 
        ff = open(file_input)
        #delim='\n'
        df = pd.read_csv(file_input,delimiter=delim,header=0,error_bad_lines=False)
        print df
        return df
    
    if dataset == "twitter":
        #ff = open(file_input)
        #h = ff.readline()
        #header_orig = h.split(delim)
        df = pd.read_csv(file_input,delimiter=delim, header=0, error_bad_lines=False)
        df.rename(columns={'Replaced Version of Main Tweet': 'text'}, inplace=True)
        '''
        if LOAD_ANNOTATIONS:
            df_selected = df[['sentence', 'annotation']]
            df_selected.columns = ['text', 'annotation']
        else:
            df.rename(columns={'Replaced Version of Main Tweet': 'text'}, inplace=True)
            #df_selected = df[['Replaced Version of Main Tweet']]
            #df_selected.columns = ['text'] 
        '''
        return df
    

def get_file_input(DATA_SET):
    if DATA_SET == "twitter":
        based_dir = data_dir+ 'Tweets/'
        file_input_name = 'tweets_textOnly_sample.txt'#'sample.csv'
        file_input = based_dir + file_input_name      
        df = read_data(file_input,"twitter",",")#read the input sentences
        texts = df['text'].tolist()

    if DATA_SET == "sentence_only":
        based_dir = data_dir+ 'Tweets/'
        file_input_name = 'tweets_textOnly.txt'#'sample.csv'
        file_input = based_dir + file_input_name      
        df = read_data(file_input,"sentence_only","\n")#read the input sentences
        texts = df['text'].tolist()  

    elif DATA_SET == "mothering":
        based_dir = data_dir + 'Vaccination/'
        file_input_name = 'sents.txt'
        #file_input_name = 'sent_cdb_child_exemption.txt'
        file_input = based_dir + file_input_name
        # file_input is extra - should be removed later

    return file_input
    
def save_pairwise_rels(file_loc,g,print_option=True):
    f = open(file_loc,'w')
    nodes = g.nodes()
    for n1 in nodes:
        for n2 in nodes:
            if n1 is not n2:
                l = g.get_edge_data(n1,n2)
                if l:
                    line = str(n1) + "\t" + str(n2) + "\t" + str(l) + "\n"
                    f.write(line)
                    if print_option:
                        print n1,n2,l    
    f.close()
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
        print ">Extraction Number: ",ind+1, " - ", "Pattern: ", r["type"]," - relation : (", r["arg1"], ", ", r["rel"], ", ", r["arg2"] ,")"
    print " ----- Extra: arg1_prep: ", r["arg1_prepositions"], " rel_prep: ", r["rel_prepositions"], " arg2_prep: ", r["arg2_prepositions"] ,"\n"

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
        
def print_top_relations(all_rels,output_file, top_num=-1):
    f = open(output_file, 'w')
    cnt = Counter()
    for r in all_rels:
        cnt[r] += 1
    if top_num == -1: # means print all
        print >>f, "Frequent relations:"
        for letter,count in cnt.most_common():
            print >>f, letter, ": ", count
    else:
        print >>f, "top ", top_num, " frequent relations:"
        for letter,count in cnt.most_common(top_num):
            print >>f, letter, ": ", count                 

def save_pairwise_relations_with_node_selection(df_rels,entity_versions,output_file):
    f = open(output_file, 'w')
    cnt = Counter()
    for entity in entity_versions:
        print >>f, "-------------------------"
        print >>f, "       ", entity
        print >>f, "-------------------------"    
        for ent_one_version in entity_versions[entity]:
            print >>f, "\n\n**** ", ent_one_version, " ****"
            df_all_versions = defaultdict(list)
            df_one_version = df_rels[np.logical_or(df_rels['arg1'].str.contains(ent_one_version),df_rels['arg2'].str.contains(ent_one_version))]
            list_one_version = df_one_version['rel'].tolist()
            for r in list_one_version:
                cnt[r] += 1
            print >>f, "Frequent relations:"
            for letter,count in cnt.most_common():
                print >>f, letter, ": ", count             
            
def get_top_entities(df_rels, output_file=None, top_num=-1, save_to_file=False):
    entities = list(df_rels['arg1']) + list(df_rels['arg2'])
    cols = ['entity', 'frequency']
    df_entity_rankings = pd.DataFrame(columns = cols)
    cnt = Counter()
    for e in entities:
        cnt[e] += 1
    if top_num == -1: # means print all
        #print "Frequent relations:"
        for letter,count in cnt.most_common():
            #print letter, ": ", count
            df_entity_rankings.loc[len(df_entity_rankings)] = [letter, count]
    else:
        #print "top ", top_num, " frequent relations:"
        for letter,count in cnt.most_common(top_num):
            #print letter, ": ", count 
            df_entity_rankings.loc[len(df_entity_rankings)] = [letter, count]

    if output_file is not None and save_to_file:
        f = open(output_file, 'w')
        df_entity_rankings.to_csv(output_file,sep=',', encoding='utf-8',header=True, columns=cols)      
        
    return df_entity_rankings


def print_full(df):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

def error_msg(error_type):
    if error_type == "tokenizer":
        return "Tokenizer failed during parsing, Ex. there might be a dash in the sentence!"
    
    
def get_entity_versions(dataset="mothering"):
    entity_versions = defaultdict(list)
    if dataset=="mothering":
        entity_versions['parents'] = ['parents', 'parent', 'i', 'we' , 'us']#, 'you']
        entity_versions['children'] = ['child', 'kid', 'kids', 'children', 'daughter', 'daughters',
                                       'son', 'sons', 'toddler',
                                       'toddlers', 'kiddo', 'boy','dd','ds']
        entity_versions['medical prof'] = ['doctor', 'doctors', 'pediatrician', 
                                           'pediatricians', 'nurse', 'nurses', 'ped', 'md', 'dr']
        entity_versions['government'] = ['government', 'cdc', 'federal', 'feds',
                                         'center for disease control', 'officials',
                                         'politician', 'official', 'law']
        entity_versions['religous inst'] = ['faith', 'religion', 'pastor', 'pastors',
                                            'parish', 'parishes', 'church', 'churches',
                                            'congregation', 'congregations', 'clergy']
        entity_versions['schools'] = ['teacher', 'teachers', 'preschools', 'preschool', 
                                      'school', 'schools', 'class', 
                                      'daycare', 'daycares', 'classes']
        entity_versions['vaccines'] = ['vaccines', 'vax', 'vaccine', 'vaccination', 
                                       'vaccinations', 'shots', 'shot', 'vaxed',
                                       'unvax', 'unvaxed', 'nonvaxed', 'vaccinate',
                                       'vaccinated', 'vaxes', 'vaxing', 'vaccinating',
                                       'substances', 'ingredients']
        entity_versions['exemptions'] = ['exemption', 'exempt']
        entity_versions['VPDs'] = ['varicella', 'chickenpox', 
                                   'flu', 'whooping cough', 'tetanus', 'pertussis', 
                                   'hepatitis', 'polio', 'mumps', 'measles', 'diphtheria']
        entity_versions['adverse effects'] = ['autism', 'autistic', 'fever', 'fevers',
                                              'reaction', 'reactions', 'infection', 'infections', 'inflammation', 'inflammations',
                                              'pain', 'pains', 'bleeding', 'bruising', 'diarrhea', 'diarrhoea']
        
    if dataset=="twitter":
        entity_versions['ApplePay'] = ['apple pay', 'apple Pay']
        entity_versions['SamsungPay'] = ['samsung pay', 'samsung Pay']
        entity_versions['googlewallet'] = ['google wallet', 'google Wallet']
        entity_versions['MasterCard'] = ['master card', 'master Card']
        entity_versions['Barclaycard'] = ['barclay card', 'barclay Card']
        entity_versions['McDonalds'] = ['mc donalds', 'mc Donalds']
        entity_versions['riteaid'] = ['rite aid', 'rite Aid']
        entity_versions['Barclays'] = ['barclaysuk', 'barclaysukhelp', 'barclays', 'barclaysbank']
        entity_versions['HSBC'] = ['hsbc_uk_press', 'hsbc_us', 'hsbc', 'hsbc_aus_Press', 'hsbc_uk', 'hsbc_uk_help', 'hsbc_uk', 'hsbc_aus_help', 'hsbc_group', 'hsbc_us_help', 'hsbc_now', 'hsbc']
        entity_versions['PayPal'] = ['paypal', 'paypaluk', 'paypalde', 'paypalin', 'askpaypal', 'paypal', 'paypal']
        entity_versions['YouTube'] = ['YouTube']
        entity_versions['Amex'] = ['askamexuk', 'askamex', 'askamex', 'amex', 'askamexau', 'amexau', 'amexuk']
        entity_versions['Starbucks'] = ['starbucks', 'starbucksru', 'starbucksuk']
        
    if dataset=="goodreads-Hobbit":
        entity_versions['hobbit'] = ["hobbit", "hobbits"]
        entity_versions['bilbo'] = ["bilbo", "baggins", "the hobbit", "burglar"]
        entity_versions['dwarf'] = ["dwarf", "dwarves", "dwarvs", "dwarfs", "thorin", "kili", "fili", "bombur"]
        entity_versions['tolkien'] = ["tolkien", "tolkein"]
        entity_versions['ring'] = ["ring", "the ring"]
        entity_versions['gandalf'] = ["gandalf", "wizard", "gandolf"]
        entity_versions['dragon'] = ["dragon", "smaug"]
        entity_versions['goblin'] = ["goblin", "goblins"]
        entity_versions['elf'] = ["elf", "elves", "elvs", "elfs"]
        entity_versions['wood-elves'] = ["wood-elves", "wood elves", "woodelves", "woodelvs", "woodelfs"]
        entity_versions['treasure'] = ["treasure", "treasures"]
        entity_versions['gollum'] = ["gollum", "smeagol", "smagol", "smegol"]
        entity_versions['bard'] = ["bard", "archer"]
        entity_versions['human'] = ["human", "humans", "man", "men", "lake-men"]
        entity_versions['laketown'] = ["laketown", "lake-town", "lake town", "village"]
        entity_versions['warg'] = ["warg", "wolves", "wolf", "wolverine", "wolverines"]
        entity_versions['arkenstone'] = ["arkenstone", "gem"]
        entity_versions['beorn'] = ["beorn", "bear"]
        entity_versions['mountain'] = ["mountain", "mountains"]
        
    if dataset=="goodreads-Frankenstein":
        entity_versions['monster'] = ['monster', 'monsters', 'monsterous']
        entity_versions['frankenstein'] = ['frankenstein','frankensteins','victor','victors', 'victor_frankenstein', 'victor_frankensteins', 'victor frankenstein']
        entity_versions['creature'] = ['creature','creatures']
        entity_versions['creation'] = ['creation','creations','creationism']
        entity_versions['god'] = ['creator','creators', 'god']
        entity_versions['mary shelley'] = ['mary_shellei', 'mary_shelley','mary','shellei','shelley','mary shellei', 'mary shelley', 'author']
        entity_versions['man'] = ['man','mans']
        entity_versions['novel'] = ['novel','novelization','stori','stories','tale', 'story', 'book']
        entity_versions['human'] = ['human','humane','humanity','humans','humanness']
        entity_versions['life'] = ['life','lifes','life.']
        entity_versions['death'] = ['death','deaths']       
        entity_versions['revenge'] = ['revenge','reveng']
        entity_versions['letter'] = ['letter','letters']
        entity_versions['elizabeth'] = ['elizabeth']
        entity_versions['walton'] = ['Walton']
        entity_versions['henry'] = ['henry']
        entity_versions['doctor'] = ['doctor']
        entity_versions['dracula'] = ['dracula']
        
        

        
    return entity_versions
        
    
def change_nt_to_not(sent):
    sent = sent.replace(" can't ", " cannot ").replace(" won't ", " will not ")
    res_sent = ""
    ind = 0
    while ind < len(sent):
        # current character
        c = sent[ind]
        # avoid out of range access.
        if ind > len(sent)-3:
            res_sent += c
            ind += 1
            continue
        # n't at the end of the sentence.
        if ind == len(sent)-3 and c == "n" and sent[ind+1] == "'" and sent[ind+2] == "t":
            res_sent += " not"
            break
        if ind == len(sent)-4 and c == "n" and sent[ind+1] == "'" and sent[ind+2] == "t":
            res_sent += " not" + sent[ind+3]
            break            
        if c == "n" and sent[ind+1] == "'" and sent[ind+2] == "t" and sent[ind+3] == " ":
            res_sent += " not "
            ind += 4
            continue
        if c == "n" and sent[ind+1] == "'" and sent[ind+2] == "t" and sent[ind+3] == ".":
            res_sent += " not."
            ind += 4
            continue            
        res_sent += c
        ind += 1
    return res_sent

def change_multi_dots_to_single_dot(sent):
    ind = 0
    res_sent = ""
    while ind < len(sent):
        c = sent[ind]
        if c == ".":
            res_sent += c
            ind2 = ind
            while ind2 < len(sent) and sent[ind2] == ".":
                ind2 += 1
            if ind2 < len(sent) and sent[ind2] != " ":
                res_sent += " "
            ind = ind2
            
        else:
            ind += 1
            res_sent += c
    return res_sent
            

def clean_sent(sent):
    '''
    This function 
            1. Replace - with .
            2. Remove punctuations - except ".", ",", ":".
            3. Change n't to not
    '''
    
    sent = sent.replace("-",".")#.replace("(","").replace(")","")
    exclude = set(string.punctuation) - {".",",",";", "!", "?", "'"}
    sent = ''.join(ch for ch in sent if ch not in exclude)    
    sent = change_nt_to_not(sent)
    sent = change_multi_dots_to_single_dot(sent)
    return sent

