'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.WME import WME
from icse.rete.ReteNode import ReteNode
from icse.rete.NccPartnerNode import NccPartnerNode
from icse.rete.NccNode import NccNode
from icse.rete.NegativeNode import NegativeNode
from icse.rete.NegativeJoinResult import NegativeJoinResult

class Token(object):
    '''
    Token: rappresenta una sequenza di wme in maniera incrementale.
    Ogni sequenza viene rappresentata come l'aggiunta di una nuova wme
    ad un precendente token:
    token< token< token< dummytoken< wme>, wme>, wme>, wme>
    '''


    def __init__(self, node, parent, w):
        '''
        Costruisce un nuovo token appartenente ad un nodo. Partendo da 
        un token padre e aggiungendo una nuova wme alla sequenza
        
        @param node: ReteNode
        @param parent: Token
        @param w: WME 
        '''
        assert isinstance(parent, Token), \
            "parent non e' un Token"
        assert isinstance(w, WME), \
            "w non e' una WME"
        assert isinstance(node, ReteNode), \
            "node non e' un ReteNode"
        
        self.__parent = parent
        self.__wme = w
        # e' probabile che questo vada riferito ad una BetaMemory/Join direttamente
        self.__node = node
        
        # lista di Token
        self.__children = []
        # lista di NegativeJoinResults
        self.__njresults = []
        # lista di Token per ncc
        self.__nccresults = []
        # solo per token in NCC partner
        # e' di tipo Token
        self.__owner = None
        
        # prepara tutti i riferimenti incrociati che servono per la
        # tree-based removal
        self.__parent._add_child(self)
        self.__wme.add_token(self)
        
        
    def get_wme(self):
        return self.__wme
    
        
    def delete(self):
        '''
        Cancella questo token e tutti i discendenti
        dalla rete. Gestisce anche l'eventuale rivalutazione
        dei nodi Ncc nel caso in cui la rimozione di questo token
        dovesse richiedere l'attivazione del nodo 
        '''
        #riferimento:
        #    delete-token-and-descendents pagina 51 [modificato]
        
        while len(self.__children) > 0 :
            child = self.__children.pop(0)
            # ricorsione... distrugge ogni figlio
            child.delete()
            del child
        
        # TODO valutare aggiunta di TokenStorage per l'interfaccia remove_token
        if not isinstance(self.__node, NccPartnerNode):
            self.__node.remove_token(self)
        
        # rimuove il riferimento a questo token che c'e' nella wme
        if self.__wme != None:
            self.__wme.remove_token(self)
            
        # rimuove il riferimento a questo token dalla lista dei figli del padre
        self.__parent._remove_child(self)
        
        # valuta casi speciali per i nodi negativi
        if isinstance(self.__node, NegativeNode):
            # rimuove tutte le njr generate da questo token
            # uso while al posto di jr in modo
            # che il riferimento a jr venga eliminato
            # dall'array
            # Penso possa essere utile per il garbage collector
            while len(self.__njresults) > 0:
                jr = self.__njresults.pop(0)
                assert isinstance(jr, NegativeJoinResult), \
                    "jr non e' un NegativeJoinResult"
                jr.get_wme().remove_njresult(jr)
                del jr
                    
        elif isinstance(self.__node, NccNode):
            # pulisce i risultati ncc correlati all'esistenza di questo token
            while len(self.__nccresults) > 0:
                rtok = self.__nccresults.pop(0)
                rtok.__wme.remove_token(rtok)
                rtok.__parent._remove_child(rtok)
                del rtok
            
        elif isinstance(self.__node, NccPartnerNode):
            # rimuove questo token dalla lista dei risultati parziali
            # e chiama la rivalutazione del nodo
            # (in modo che se non ci siano match l'evento venga propagato)
            assert isinstance(self.__node, NccPartnerNode)
            if self.__owner._remove_nccresult(self):
                # devo rivalutare
                self.__node.get_nccnode().revalutate(self.__owner)
        
    def deleteDescendents(self):
        '''
        Rimuove tutti i discendenti di questo token
        dalla rete
        '''
        while len(self.__children) > 0:
            self.__children.pop(0).delete()
            
    def _add_child(self, t):
        self.__children.insert(0, t)
        
    def _remove_child(self, t):
        self.__children.remove(t)
        
    def _remove_nccresult(self, t):
        self.__nccresults.remove(t)
        return (len(self.__nccresults) == 0) 