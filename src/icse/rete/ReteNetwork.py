'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.WME import WME
from icse import rete
from icse.rete.Nodes import AlphaRootNode, ReteNode
from icse.rete.PNode import PNode
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper
from icse.rete.Agenda import Agenda
from icse.debug import EventManager


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
        self.__agenda = Agenda()
        self.__wme_nextid = 0
        
        self.__alpha_root = AlphaRootNode(self)
        #self.__beta_root = BetaRootNode(self, self.__alpha_root)
        #self.__alpha_root.get_alphamemory().add_successor(self.__beta_root)
        
        EventManager.trigger(EventManager.E_NODE_ADDED, self.__alpha_root)        
        
        #NetworkXGraphWrapper.i().add_node(self.__alpha_root, None)
        #Ubigraph.i().add_node(self.__alpha_root.get_alphamemory(), self.__alpha_root)
        #Ubigraph.i().add_node(self.__beta_root, self.__alpha_root, 1)
        
    def get_root(self):
        return self.__alpha_root
        
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
            EventManager.trigger(EventManager.E_FACT_ASSERTED, wme, False)
            
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

            EventManager.trigger(EventManager.E_FACT_ASSERTED, wme, True)
            
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
        del self.__wmes_map[self._get_fact_dict_key(wme.get_fact())]
        
        #import sys
        #print >> sys.stderr, "Sto ritrattando: ", wme
        
        wme.remove()
        
        EventManager.trigger(EventManager.E_FACT_RETRACTD, wme)
        
        del wme
        
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
                      production.get_properties(),
                      symbols,
                      onActive=self.__agenda.insert,
                      onDeactive=self.__agenda.remove,
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

        EventManager.trigger( EventManager.E_NODE_ADDED, pnode)
        
        EventManager.trigger( EventManager.E_NODE_LINKED, pnode, last_node, -1)
        
        EventManager.trigger( EventManager.E_RULE_ADDED, production, pnode)
        
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

        EventManager.trigger( EventManager.E_RULE_REMOVED, pnode_or_rulename)
        
    def agenda(self):
        return self.__agenda
    
