'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.WME import WME
from icse import rete
from icse.rete.Nodes import AlphaRootNode, ReteNode
from icse.rete.PNode import PNode
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper


class ReteNetwork(object):
    '''
    Implementazione di un network di tipo Rete
    per il pattern matching delle produzioni
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__wmes_map = {}
        self.__id_fact_map = {}
        self.__rules_map = {}
        self.__activables = []
        self.__wme_nextid = 0
        
        self.__alpha_root = AlphaRootNode(self)
        #self.__beta_root = BetaRootNode(self, self.__alpha_root)
        #self.__alpha_root.get_alphamemory().add_successor(self.__beta_root)
        
        NetworkXGraphWrapper.i().add_node(self.__alpha_root, None)
        #Ubigraph.i().add_node(self.__alpha_root.get_alphamemory(), self.__alpha_root)
        #Ubigraph.i().add_node(self.__beta_root, self.__alpha_root, 1)
        
        
    def get_wmes(self):
        return self.__wmes_map.values()
        
    def _get_fact_dict_key(self, fact):
        if isinstance(fact, list):
            return tuple(fact)
        elif isinstance(fact, dict):
            return tuple(fact.items())
        else:
            return fact
        
    def get_wme(self, fact_or_fact_id):
        if isinstance(fact_or_fact_id, int):
            # e' un id
            fact_or_fact_id = self.__id_fact_map[fact_or_fact_id]
            
        return self.__wmes_map[self._get_fact_dict_key(fact_or_fact_id)]
        
    def assert_fact(self, fact):
        '''
        Asserisce un nuovo fatto nel network
        @param fact: Fact
        '''
        
        try:
            wme = self.get_wme(fact)
            # se l'ho trovato (e quindi niente eccezione
            # significa che e' un duplicato
            # ergo non propago nulla
            return (wme.get_factid(), wme, False)
            
        except KeyError:
            
            # se non l'ho trovato, devo asserire realmente
            fact_dict_key = self._get_fact_dict_key(fact)
            
            wme = WME(fact)
        
            # e' un nuovo WME, quindi incremento l'id...
            self.__wme_nextid += 1

            # inserisco nella map wme -> ID
            self.__wmes_map[fact_dict_key] = wme
            
            wme.set_factid(self.__wme_nextid)
            
            self.__id_fact_map[self.__wme_nextid] = fact_dict_key
            
            # ...e propago
            self.__alpha_root.activation(wme)
            
            return (self.__wme_nextid, wme, True)
        
        
    def retract_fact(self, wme):
        '''
        Ritratta un fatto dal network
        @param wme: WME una wme gia presente nella rete 
        '''
        
        if not isinstance(wme, WME):
            # la cerco nel dizionario wme
            wme = self.__wmes_map[self._get_fact_dict_key(wme)]
            
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        # rimuovo dalla mappa wme -> id
        # (questo mi assicura che la wme ci sia)
        self.__wmes_map.pop(self._get_fact_dict_key(wme.get_fact()))
        
        #import sys
        #print >> sys.stderr, "Sto ritrattando: ", wme
        
        wme.remove()
        
    def add_production(self, production):
        '''
        Aggiunge una nuova produzione al network
        @param production: Production
        '''
        symbols = {}
        last_node = rete.network_factory(self.__alpha_root, None, production.get_lhs(), builtins=symbols)
        
        #from pprint import pprint
        #pprint(symbols, indent=4)
        
        pnode = PNode(last_node,
                      production.get_name(),
                      production.get_rhs(),
                      symbols,
                      onActive=self.add_activable,
                      onDeactive=self.remove_activable,
                      assertFunc=self.assert_fact,
                      retractFunc=self.retract_fact,
                      addProduction=self.add_production,
                      removeProduction=self.remove_production
                )
        assert isinstance(last_node, ReteNode), \
            "last_node non e' un ReteNode"
            
        last_node.add_child(pnode)
        
        last_node.update(pnode)
        
        NetworkXGraphWrapper.i().add_node(pnode, last_node, -1)
        
        self.__rules_map[production.get_name] = pnode
        
        return pnode
        
        
    def remove_production(self, pnode_or_rulename):
        '''
        Rimuove una produzione dal network
        @param pnode_or_rulename: PNode
        '''
        if not isinstance(pnode_or_rulename, PNode):
            pnode_or_rulename = self.__rules_map[pnode_or_rulename]
            
        assert isinstance(pnode_or_rulename, PNode)
        
        del self.__rules_map[pnode_or_rulename.get_name()]
        
        pnode_or_rulename.delete()
        
        
    def add_activable(self, pnode, token ):
        '''
        Aggiunge un nuovo elemento <PNode, token>
        alla lista delle produzioni attivabili
        '''
        #print "Nuova regola attivabile: {0} => {1}".format(pnode.get_name(), token.linearize())
        self.__activables.append( (pnode, token) )
        
    def remove_activable(self, pnode, token ):
        '''
        Rimuove un elemento <PNode, token> dalla
        lista di produzioni attivabili
        '''
        self.__activables.remove((pnode, token))
        
    def agenda(self):
        return self.__activables
    
