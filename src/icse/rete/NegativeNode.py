'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.JoinNode import JoinNode
from icse.rete.ReteNode import ReteNode
from icse.rete.AlphaMemory import AlphaMemory
from icse.rete.Token import Token
from icse.rete.NegativeJoinResult import NegativeJoinResult
from icse.rete.WME import WME

class NegativeNode(JoinNode):
    '''
    JoinNode per condizioni negative
    '''


    def __init__(self, parent, amem, tests):
        '''
        Constructor
        '''
        
        # lista di Token
        self.__items = []
        
        # amem e tests dal JoinNode come proprieta' "protette"
        # self._amem
        # self._tests
        JoinNode.__init__(self, parent, amem, tests)
        
    def get_items(self):
        '''
        Restituisce la lista di match (come fosse una beta-memory)
        @return: Token[]
        '''
        return self.__items
    
    def remove_item(self, tok):
        '''
        Rimuove un token dagli items
        '''
        self.__items.remove(tok)
    
        
    @staticmethod
    def factory(parent, amem, tests):
        
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"

        for child in parent.get_children():
            if  isinstance(child, NegativeNode):
                #assert isinstance(child, JoinNode)
                if child._amem == amem:
                    if child.__tests == tests:
                        # stessi test, testa amem... condivido il nodo
                        return child
                
        # non posso condividere un nuovo gia esistente
        # con queste informazioni, quindi ne creo uno nuovo
        # e lo aggiunto alla rete
        
        njn = NegativeNode(parent, amem, tests)
        parent.add_child(njn)
        amem.add_successor(njn)
        
        # aggiorna
        parent.update(njn)
        
        return njn

    def leftActivation(self, tok, wme):

        assert isinstance(wme, WME), \
            "wme non e' un WME"
        
        new_token = Token(self, tok, wme)
        
        self.__items.insert(0, new_token)
        
        for w in self._amem.get_items():
            if self._perform_tests(w, new_token):
                njr = NegativeJoinResult(new_token, w)
                
                new_token.add_njresult(njr)
                wme.add_njresult(njr)
                
        # attiva solo se non ci sono match (e' un nodo negativo)
        if new_token.count_njresults() == 0 :
            for child in self.__children:
                assert isinstance(child, ReteNode), \
                    "child non e' un ReteNode"
                    
                # attenzione, la leftActivation viene fornita senza la WME
                # quindi solo i join node sono preparati a riceverla?????
                # TODO refactoring
                child.leftActivation(new_token)
        
        
    def rightActivation(self, wme):
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        for t in self.__items:
            assert isinstance(t, Token), \
                "t non e' un Token"
                
            if self._perform_tests(wme, t):
                # controllo se prima c'erano match
                if t.count_njresults() == 0:
                    # se non c'erano match
                    # allora il token e' stato propagato
                    # e quindi devo revocarlo
                    t.deleteDescendents()

                # creo il NegativeJoinResult
                njr = NegativeJoinResult(t, wme)
                
                t.add_njresult(njr)
                wme.add_njresult(njr)
    
    def update(self, child):
        '''
        Esegue l'aggiornamento dei figli (attivandoli a sinistra)
        se vengono trovati token che non hanno match per njresult
        (il nodo e' negativo)
        '''
        for t in self.__items:
            assert isinstance(t, Token), \
                "t non e' un Token"
                
            if t.count_njresults() == 0:
                child.leftActivation(t)

    def delete(self):
        '''
        Esegue la rimozione del nodo dalla rete,
        pulendo la memoria interna del nodo
        '''
        
        # questo codice e' identico
        # a quello per la pulizia della BetaMemory
        # ma questo elemento non e' derivato
        # ho cercato di evitare da doppia ereditariera'
        while len(self.__items) > 0:
            tok = self.__items.pop(0)
            assert isinstance(tok, Token), \
                "tok non e' un Token"
                
            tok.delete()
        
        JoinNode.delete(self)
    
    
    
    