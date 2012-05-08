'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.ReteNode import ReteNode
from icse.rete.Token import Token

class BetaMemory(ReteNode):
    '''
    Beta Memory node: contiene la lista di token che matchano un particolare
    insieme di condizioni con intra-riferimenti di variabili
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        ReteNode.__init__(self, parent)
        
        # lista di token mantenuti nella beta memory
        self.__items = []
        
    def get_items(self):
        return self.__items
    
    def leftActivation(self, tok, wme):
        
        new_token = Token(self, tok, wme)
        self.__items.insert(0, new_token)
        
        for child in self.__children:
            assert isinstance(child, ReteNode), \
                "child non e' un ReteNode"
                
            # attenzione, la leftActivation viene fornita senza la WME
            # quindi solo i join node sono preparati a riceverla?????
            # TODO refactoring
            child.leftActivation(tok)
            
        
    def delete(self):
        '''
        Cancella tutti i token memorizzati in questo nodo (e chiaramente i successori)
        '''
        
        while len(self.__items) > 0:
            tok = self.__items.pop(0)
            assert isinstance(tok, Token), \
                "tok non e' un Token"
                
            tok.delete()
            
        # chiama il metodo della classe base
        # per eseguire le operazioni di pulizia
        # comuni a tutti i nodi della BetaNetwork
        ReteNode.delete(self)
        
    def update(self, child):
        
        assert isinstance(child, ReteNode), \
            "child non e' un ReteNode"
        
        for tok in self.__items:
            self.leftActivation(tok)
        
    def factory(self, parent):
        
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
            
        for child in parent.get_children():
            if isinstance(child, BetaMemory):
                # semplicemente un beta memory node
                # e un contenitore senza condizioni:
                # cio che discrimina il contenuto e'
                # il join-node padre.
                # quindi se ho gia un nodo betamemory
                # figlio dello stesso padre, semplicemente
                # lo condivido
                return child
        
        # non ho trovato nessun beta-memory
        # figlio del padre, quindi ne aggiungo
        # uno nuovo
        
        bm = BetaMemory(parent)
        parent.add_child(bm)
        parent.update(bm)

        return bm