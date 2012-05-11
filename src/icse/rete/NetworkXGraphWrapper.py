'''
Created on 11/mag/2012

@author: Francesco Capozzo
'''

class NetworkXGraphWrapper(object):
    '''
    classdocs
    '''

    _instance = None

    def __init__(self):
        '''
        Constructor
        '''
        
        self._isReady = True
        self._nodemap = {}
        self._edgemap = {}
        self._G = None
        self._nodeid = 1

        try:
            import networkx as nx
            G = nx.Graph()
            self._G = G
        except:
            print "NetworkX init fallito"
            self._isReady = False

        
    @staticmethod
    def i():
        '''
        @return self
        '''
        if NetworkXGraphWrapper._instance == None:
            NetworkXGraphWrapper._instance = NetworkXGraphWrapper()
        return NetworkXGraphWrapper._instance
        

    def is_ready(self):
        return self._isReady

    def add_node(self, node, parent, linkType=0):
        if not self.is_ready():
            return self._fallback_add_node(node, parent, linkType)
        
        assert not isinstance(node, int) 
        assert not isinstance(parent, int)
        
        if not self._nodemap.has_key(node):
            
            # nuovo nodo
            self._nodemap[node] = self._nodeid
            parent_id = self._nodemap.get(parent, None)
            self._G.add_node(self._nodeid,attr_dict={
                    'type': str(node.__class__.__name__).split(".")[-1],
                    'ref': node
                })
            if getattr(node, 'get_tests', None) != None:
                tests = node.get_tests()
                self._G.node[self._nodeid]['tests'] = [repr(t) for t in tests]
             
            if str(node.__class__.__name__).split(".")[-1] == "AlphaRootNode":
                self._G.node[self._nodeid]['label'] = 'ROOT'

            if str(node.__class__.__name__).split(".")[-1] == "ConstantTestNode":
                self._G.node[self._nodeid]['label'] = '[{0}] {1} {2}'.format(node.get_field(), str(node.get_predicate().__name__).split(".")[-1], node.get_value() )

            if str(node.__class__.__name__).split(".")[-1] == "PNode":
                self._G.node[self._nodeid]['label'] = node.get_name()

            if getattr(node, 'get_items', None) != None:
                self._G.node[self._nodeid]['dyn_label'] = lambda ref:'[{0}]'.format(len(ref.get_items()))
             
            if parent_id != None:
                self.add_edge(parent_id, self._nodeid, linkType )
            
            self._nodeid += 1
                
        return self._nodemap[node]
        
    def _fallback_add_node(self, node, parent, linkType):
        
        assert not isinstance(node, int) 
        assert not isinstance(parent, int)
        
        if not self._nodemap.has_key(node):
            self._nodemap[node] = self._nodeid
            print "("+str(self._nodeid)+", "+str(node.__class__.__name__)+") Nuovo nodo"
            
            parent_id = self._nodemap.get(parent, None)
            if parent_id != None:
                self.add_edge(self._nodeid, parent_id , linkType)
                
            self._nodeid += 1
            
        return self._nodemap[node]
        
            
            
    def add_edge(self, child, parent, linkType=0):
        if not self.is_ready():
            return self._fallback_add_edge(child, parent, linkType)
        
        if child == None or parent == None:
            return
        
        if self._nodemap.has_key(child):
            child = self._nodemap[child]
        if self._nodemap.has_key(parent):
            parent = self._nodemap[parent]
        
        self._G.add_edge(parent, child)
        
        self._G.edge[parent][child]["type"] = linkType
            
            
            
    def _fallback_add_edge(self, child, parent, linkType):
        if child == None or parent == None:
            return

        triple = (parent, child, linkType)
        if not self._edgemap.has_key(triple):

            if linkType == 0:
                print str(parent)+" ---------> "+str(child)
            elif linkType < 0:
                print str(parent)+" --LEFT---> "+str(child)
            else:
                print str(parent)+" --RIGHT--> "+str(child)

            self._edgemap[triple] = True
            
    def draw(self):
        
        import networkx as nx
        import matplotlib.pyplot as plt
        #import pylab as P
        
#        pos = nx.graphviz_layout(self._G)
#        
#        plt.rcParams['text.usetex'] = False
#        plt.figure(figsize=(8,8))
#        nx.draw_networkx_edges(self._G,pos,alpha=0.3,edge_color='m')
#        nx.draw_networkx_nodes(self._G,pos,node_color='w',alpha=0.4)
#        nx.draw_networkx_edges(self._G,pos,alpha=0.4,node_size=0,width=1,edge_color='k')
#        nx.draw_networkx_labels(self._G,pos,fontsize=14)        
#        
#        font = {'color'      : 'k',
#                'fontweight' : 'bold',
#                'fontsize'   : 14}        
#        plt.title("Rete Network", font)
#        
        
        #nx.draw_graphviz(self._G)
        #nx.draw_networkx_edge_labels(self._G)
        #P.draw()
        #P.show()
        #plt.show()
        
        G = self._G
                
        eright=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] > 0]
        eleft=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] < 0]
        enormal=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] == 0]
        
        
        nroots=[n for (n,d) in G.nodes(data=True) if d['type'] == 'AlphaRootNode']
        namems=[n for (n,d) in G.nodes(data=True) if d['type'] == 'AlphaMemory']
        nctns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'ConstantTestNode']
        nbmems=[n for (n,d) in G.nodes(data=True) if d['type'] == 'BetaMemory']
        njns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'JoinNode']
        ndjns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'DummyJoinNode']
        npnodes=[n for (n,d) in G.nodes(data=True) if d['type'] == 'PNode']
        nnjns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NegativeNode']
        nccs=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NccNode']
        nccps=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NccPartnerNode']
        

        ltests=dict([(n,"\n".join(d['tests'])) for (n,d) in G.nodes(data=True) if d.has_key('tests') and len(d['tests']) > 0])
        llabels=dict([(n,d['label']) for (n,d) in G.nodes(data=True) if d.has_key('label') and not d.has_key('dyn_label')])
        lbothlabels=dict([(n,"\n".join([d['dyn_label'](d['ref']), d['label']])) for (n,d) in G.nodes(data=True) if d.has_key('label') and d.has_key('dyn_label') and callable(d['dyn_label'])])
        ldynlabels=dict([(n,d['dyn_label'](d['ref'])) for (n,d) in G.nodes(data=True) if d.has_key('dyn_label') and ( not d.has_key('label') ) and callable(d['dyn_label'])])

        
        pos=nx.graphviz_layout(G, root=nroots[0]) # positions for all nodes
        
        # nodes
        #nx.draw_networkx_nodes(G,pos,node_size=600)

        # differenzio i nodi per tipo
        # ROOT
        nx.draw_networkx_nodes(G,pos,nodelist=nroots,
                               node_size=1000,alpha=0.7)
        
        # CONSTANT TEST NODE
        nx.draw_networkx_nodes(G,pos,nodelist=nctns,
                               node_size=600,alpha=0.7,node_color='w')

        # ALPHA MEMORIES
        nx.draw_networkx_nodes(G,pos,nodelist=namems,
                               node_size=600,alpha=0.7,node_color='y',node_shape='s')

        # DUMMY JOINS
        nx.draw_networkx_nodes(G,pos,nodelist=ndjns,
                               node_size=300,alpha=0.7,node_color='b',node_shape='o')
        
        # JOINS
        nx.draw_networkx_nodes(G,pos,nodelist=njns,
                               node_size=900,alpha=0.7,node_color='w',node_shape='v')

        # BETA MEMORIES
        nx.draw_networkx_nodes(G,pos,nodelist=nbmems,
                               node_size=600,alpha=0.7,node_color='r',node_shape='s')
        
        # NEGATIVE JOINS
        nx.draw_networkx_nodes(G,pos,nodelist=nnjns,
                               node_size=900,alpha=0.7,node_color='w',node_shape='^')
        
        # PNODES
        nx.draw_networkx_nodes(G,pos,nodelist=npnodes,
                               node_size=900,alpha=0.7,node_color='w',node_shape='8')
        
        
        
        
        # edges
        nx.draw_networkx_edges(G,pos,edgelist=eright,
                            width=3,alpha=0.5,edge_color='r')
        nx.draw_networkx_edges(G,pos,edgelist=eleft,
                            width=3,alpha=0.5,edge_color='g')
        nx.draw_networkx_edges(G,pos,edgelist=enormal,
                            width=3,alpha=0.5,edge_color='b',style='dashed')
        
        
        # labels
        nx.draw_networkx_labels(G,pos,labels=ltests,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=llabels,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=lbothlabels,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=ldynlabels,font_size=10)
        
        plt.axis('off')
        #plt.savefig("weighted_graph.png") # save as png
        plt.show() # display        
        
        
        

            