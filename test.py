import os
import graphviz


os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

path_current = os.path.dirname(__file__)
path_graph = os.path.join(path_current, "build", "graph")
path_svg = os.path.join(path_current, "test.svg")


g = graphviz.Graph('G', filename=path_graph)
g.attr(bgcolor='purple:pink', label='agraph', fontcolor='white')

with g.subgraph(name='cluster1') as c:
    c.attr(fillcolor='blue:cyan', label='acluster', fontcolor='white',
           style='filled', gradientangle='270')
    c.attr('node', shape='box', fillcolor='red:yellow',
           style='filled', gradientangle='90')
    c.node('anode')

g.view()