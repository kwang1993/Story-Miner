
# coding: utf-8

# In[2]:

import time # to calculate the annotation time
import re # regular expression
import networkx as nx # to calculate the shortest path between nodes in the parsing tree
from practnlptools.tools import Annotator # to extract dep_parse, syntatic_parse, srl, verbs, words, POS, NER, chunks
import pandas as pd
from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from pprint import pprint # print dictionaries nicer
from nxpd import draw # show in iptyhon
from IPython.display import display # to display images and draw objects 
from networkx.drawing.nx_agraph import write_dot
import sys

try:
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")

get_ipython().magic(u'matplotlib inline')

#import the other functions
get_ipython().magic(u"run -i 'main_functions'")
get_ipython().magic(u"run -i 'utility_functions'")
get_ipython().magic(u"run -i 'parameters'")

annotator = Annotator()

'''
A few sample test cases:
#texts = ["the Church told all Catholic parents not to let their child get the MMR."]
#texts = ["Why Samsung Pay could gain an early lead in mobile payments."]
#texts = ["You would keep your child 's shot records at home and NOT submit that to the school...only your exemption from all shots ."]
#texts = ["Parents may use their philosophical beliefs exemption for ANY vaccine they choose to do so ; you may selectively vaccinate your child and exempt them out of other vaccines ; you may also exempt out of any and all vaccines and use your exemption that way , as well ."]
#texts = ["Here is the Hawaii immunization brochure , which states the exemption forms can also be obtained from the school : Immunization and TB code : Surprisingly , I do n't see anything about religiously exempting a child from the TB screening requirement in the code ."]
'''
texts = ['Here is a link to the DOH exemption page : Your statement should read : Our child , [ FULL NAME ] will be entering [ NAME OF SCHOOL ] as a kindergartener this Fall and we are submitting this statement in order to satisfy state immunization requirements for school entry .\n\nKatherine You only submit a religious exemption to the school district once your child starts school , or to their daycare if they go there or preschool , etc .\n\n: My son was previously vaxed and we submitted an exemption letter just this year and it was accepted .\n\n) Even though my 6 yr. old son is not required to receive the next  mandatory " vaccination until 7th grade ( six years from now ) , I wanted to know if I should submit a request for a religious exemption NOW since I am pregnant and do not plan on vaccinating the new baby .']
all_rels = []
start_time = time.time()
for ind, t in enumerate(texts):
    #if ind > 500:
    #    break
    print ind, t
    try:
        t_annotated = annotator.getAnnotations(t, dep_parse=True)
    except:
        print "Error in sentence annotation"
    try:
        g_dir = create_dep_graph(t_annotated)
        if g_dir is None:
            print "No extraction found"
            continue
        plot_dep(g_dir,t)
        g_undir = g_dir.to_undirected()
        rels = get_relations(g_dir, t_annotated, option="SVO")
        print_relations(rels) 
        all_rels = all_rels + get_rels_str(rels)        
    except:
        print "Unexpected error while extracting relations:", sys.exc_info()[0]


end_time = time.time()
print "Relation Extraction Time: ", end_time-start_time , "(seconds) - ", (end_time-start_time)/60, "(min)"
    
print "***************STATISTICS***************"
print "Total number of input records (posts): ", len(texts)
print "Total number of extracted relations: ", len(all_rels)
print_arguments_graph(all_rels,top_num=10) 
print "All relations:"
print all_rels


# In[6]:

texts = ['Here is a link to the DOH exemption page : Your statement should read : Our child , [ FULL NAME ] will be entering [ NAME OF SCHOOL ] as a kindergartener this Fall and we are submitting this statement in order to satisfy state immunization requirements for school entry .\n\nKatherine You only submit a religious exemption to the school district once your child starts school , or to their daycare if they go there or preschool , etc .\n\n: My son was previously vaxed and we submitted an exemption letter just this year and it was accepted .\n\n) Even though my 6 yr. old son is not required to receive the next  mandatory " vaccination until 7th grade ( six years from now ) , I wanted to know if I should submit a request for a religious exemption NOW since I am pregnant and do not plan on vaccinating the new baby .']
t = texts[0]
print t
t_annotated = annotator.getAnnotations(t, dep_parse=True)
print t_annotated


# In[ ]:



