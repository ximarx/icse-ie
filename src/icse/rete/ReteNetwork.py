'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.WME import WME
from icse import rete
from icse.rete.Nodes import AlphaRootNode, BetaRootNode, ReteNode
from icse.rete.PNode import PNode


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
        self.__rules_map = {}
        self.__activables = []
        self.__wme_nextid = 0
        
        self.__alpha_root = AlphaRootNode(self)
        self.__beta_root = BetaRootNode(self, self.__alpha_root)
        
    def get_wmes(self):
        return self.__wmes_map.keys()
        
    def assert_fact(self, fact):
        '''
        Asserisce un nuovo fatto nel network
        @param fact: Fact
        '''

        # converte il fatto in una WME
        wme = WME([])
        
        # controllo che non sia un duplicato
        if not self.__wmes_map.has_key(wme):
        
            # e' un nuovo WME, quindi incremento l'id...
            self.__wme_nextid += 1

            # inserisco nella map wme -> ID
            self.__wmes_map[wme] = self.__wme_nextid
            
            # ...e propago
            self.__alpha_root.activation(wme)
            
            return (self.__wme_nextid, wme, True)

        else:
            # e' un duplicato
            # restituisco quella che gia c'e'
            # indicando che non e' una nuova aggiunta
            return (self.__wmes_map[wme], wme, False)
        
        
    def retract_fact(self, wme):
        '''
        Ritratta un fatto dal network
        @param wme: WME una wme gia presente nella rete 
        '''
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        # rimuovo dalla mappa wme -> id
        # (questo mi assicura che la wme ci sia)
        self.__wmes_map.pop(wme)
        
        wme.remove()
        
    def add_production(self, production):
        '''
        Aggiunge una nuova produzione al network
        @param production: Production
        '''
        symbols = {}
        last_node = rete.network_factory(self.__alpha_root, self.__beta_root, production.get_lhs(), builtins=symbols)
        
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
        
        
    def remove_production(self, pnode):
        '''
        Rimuove una produzione dal network
        @param pnode: PNode
        '''
        
    def add_activable(self, pnode, token ):
        '''
        Aggiunge un nuovo elemento <PNode, token>
        alla lista delle produzioni attivabili
        '''
        self.__activables.append( (pnode, token) )
        
    def remove_activable(self, pnode, token ):
        '''
        Rimuove un elemento <PNode, token> dalla
        lista di produzioni attivabili
        '''
        self.__activables.remove((pnode, token))
        
    
