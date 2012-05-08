'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.ReteNode import ReteNode
from icse.rete.JoinTest import JoinTest
from icse.rete.AlphaMemory import AlphaMemory
from icse.rete.Token import Token
from icse.rete.WME import WME
from icse.rete.BetaMemory import BetaMemory
from icse.rete.NegativeNode import NegativeNode

class JoinNode(ReteNode):
    '''
    JoinNode: rappresenta un nodo giunzione fra uno
    proveniente dall'AlphaNetwork e uno proveniente da
    BetaNetwork 
    '''

    def __init__(self, parent, amem, tests):
        '''
        Constructor
        '''

        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"
        
        self._amem = amem
        
        # filtra tutti gli elementi non JoinTest
        self._tests = [x for x in tests if isinstance(x, JoinTest)]
        ReteNode.__init__(self, parent)
        
    
    def leftActivation(self, tok, wme = None):
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        for w in self._amem.get_items():
            if self._perform_tests(w, tok):
                for child in self.__children:
                    assert isinstance(child, ReteNode), \
                        "child non e' un ReteNode"
                    
                    # attiva a sinistra i figli
                    # (che sono betamemory o riconducibili)
                    child.leftActivation(tok, w)
    
    def rightActivation(self, wme):
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        assert isinstance(self.__parent, BetaMemory), \
            "parent non e' un BetaMemory"
            
        for tok in self.__parent.get_items():
            
            if self._perform_tests(wme, tok):
                for child in self.__children:
                    assert isinstance(child, ReteNode), \
                        "child non e' un ReteNode"
                    
                    # attiva a sinistra i figli
                    # (che sono betamemory o riconducibili)
                    
                    child.leftActivation(tok, wme)
        

    def _perform_tests(self, wme, tok):
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        assert isinstance(tok, Token), \
            "tok non e' un Token"
        
        for t in self._tests:
            
            if not t.perform(tok, wme):
                return False
        
        return True
    
    @staticmethod
    def factory(parent, amem, tests):

        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"

        for child in parent.get_children():
            # escludo che un join node possa essere condiviso da un
            # NegativeNode con gli stessi test e alpha-memory
            if isinstance(child, JoinNode) and not isinstance(child, NegativeNode):
                #assert isinstance(child, JoinNode)
                if child._amem == amem:
                    if child.__tests == tests:
                        # stessi test, testa amem... condivido il nodo
                        return child
                
        # non posso condividere un nuovo gia esistente
        # con queste informazioni, quindi ne creo uno nuovo
        # e lo aggiunto alla rete
        
        jn = JoinNode(parent, amem, tests)
        parent.add_child(jn)
        amem.add_successor(jn)
        
        return jn
        
    def delete(self):
        '''
        Esegue la cancellazione del nodo
        propagando la cancellazione all'alpha-memory
        se non e' condivisa con altri nodi
        '''
        
        self._amem.remove_successor(self)
        
        if self._amem.is_useless():
            self._amem.delete()
        
        
        ReteNode.delete(self)
        
    def update(self, child):
        
        # memorizzo temporaneamente la lista
        # attuale di figli
        saved_children = self.__children
        
        self.__children = [child]
        
        for wme in self._amem.get_items():
            assert isinstance(wme, WME), \
                "wme non e' un WME"
            
            # forzo l'aggiornamento di ogni wme che
            # verra' propagata ai figli (che in questo
            # caso sono solo quello nuovo... temporaneamente)    
            self.rightActivation(wme)
            
        # ho aggiornato il figlio, a questo punto
        # ripristino la vecchia lista
        
        self.__children = saved_children
        
        