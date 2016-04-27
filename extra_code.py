
# coding: utf-8

# In[ ]:

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
#from networkx import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import write_dot

G = nx.DiGraph()

G.add_node("ROOT")

for i in xrange(5):
    G.add_node("Child_%i" % i)
    G.add_node("Grandchild_%i" % i)
    G.add_node("Greatgrandchild_%i" % i)

    G.add_edge("ROOT", "Child_%i" % i)
    G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
    G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
#write_dot(G,'test.dot')
nx.drawing.nx_agraph.write_dot(G,'test2.dot')

# same layout using matplotlib with no labels
plt.title("draw_networkx")
pos=graphviz_layout(G,prog='dot')
nx.draw(G,pos,with_labels=False,arrows=False)
plt.savefig('nx_test.png')



# In[ ]:

from graphviz import Digraph

dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

dot


# In[ ]:

import networkx as nx
import matplotlib.pyplot as plt

try:
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")


G=nx.balanced_tree(3,5)
pos=graphviz_layout(G,prog='twopi',args='')
plt.figure(figsize=(8,8))
nx.draw(G,pos,node_size=20,alpha=0.5,node_color="blue", with_labels=False)
plt.axis('equal')
plt.savefig('circular_tree.png')
plt.show()

