'''
Created on 11/mag/2012

@author: Francesco Capozzo
'''
import xmlrpclib

class Ubigraph(object):
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
            server_url = 'http://127.0.0.1:20738/RPC2'
            server = xmlrpclib.Server(server_url)
            G = server.ubigraph
            G.clear()
            self._G = G
        except:
            print "Ubigraph init fallito"
            self._isReady = False

        
    @staticmethod
    def i():
        '''
        @return self
        '''
        if Ubigraph._instance == None:
            Ubigraph._instance = Ubigraph()
        return Ubigraph._instance
        

    def is_ready(self):
        return self._isReady

    def add_node(self, node, parent, linkType=0):
        if not self.is_ready():
            return self._fallback_add_node(node, parent, linkType)
        
        assert not isinstance(node, int) 
        assert not isinstance(parent, int)
        
        if self._nodemap.has_key(node):
            # decidero in seguito
            # per ora ignoro
            print "Nodo ignorato... gia nel grafico"
            return
        else:
            # nuovo nodo
            parent_vertex = self._nodemap.get(parent, None)
            node_vertex = self._G.new_vertex()
            self._G.set_vertex_attribute(node_vertex, "label", str(node.__class__))
            
            # aggiungo subito
            self._nodemap[node] = node_vertex
            
            # creo un nuovo collegamento
            if parent_vertex != None:
                self.add_edge(node_vertex, parent_vertex)
                
            return node_vertex
        
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
        
        triple = (parent, child, linkType)
        if not self._edgemap.has_key(triple):
            
            edge = self._G.new_edge(parent, child)
            self._G.set_edge_attribute(edge, "arrow", "true")
            
            if linkType < 0:
                # left link
                self._G.set_edge_attribute(edge, "color", "#006400")
            elif linkType > 0:
                self._G.set_edge_attribute(edge, "color", "#8b0000")
            
            
            self._edgemap[triple] = edge
            
            
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

            
    def get_vertex(self, node):
        try:
            return self._nodemap[node]
        except:
            return None 
            