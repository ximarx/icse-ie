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
        
        self.__amem = amem
        
        # filtra tutti gli elementi non JoinTest
        self.__tests = [x for x in tests if isinstance(x, JoinTest)]
        ReteNode.__init__(self, parent)
        
    
    def leftActivation(self, tok, wme = None):
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        for w in self.__amem.get_items():
            assert isinstance(w, WME), \
                "w non e' un WME"
                
            failed = False
                
            for t in self.__tests:
                assert isinstance(t, JoinTest), \
                "t non e' un JoinTest"
                
                if not t.perform(tok, w):
                    # stoppa il controllo al primo test fallito
                    failed = True
                    break
                
            if not failed:
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
            
            assert isinstance(tok, Token), \
                "tok non e' un Token"
                
            failed = False
            
            for t in self.__tests:
                
                assert isinstance(t, JoinTest), \
                "t non e' un JoinTest"
                
                if not t.perform(tok, wme):
                    failed = True
                    break
                
            if not failed:
                for child in self.__children:
                    assert isinstance(child, ReteNode), \
                        "child non e' un ReteNode"
                    
                    # attiva a sinistra i figli
                    # (che sono betamemory o riconducibili)
                    
                    child.leftActivation(tok, wme)
        
    
    @staticmethod
    def factory(parent, amem, tests):

        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"

        
        