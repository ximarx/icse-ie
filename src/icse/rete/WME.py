'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.NegativeJoinResult import NegativeJoinResult
import time


class WME(object):
    '''
    Entry della working memory
    '''


    def __init__(self, fields):
        '''
        Construisce una nuova WME utilizzando una n-upla
        per rappresentare il fatto
        '''
        self.__fields = fields
        self.__alphamemories = []
        self.__tokens = []
        self.__njresults = []
        self.__factid = 0
        
        
        self.__time = time.time()
        
    def set_factid(self, newid):
        self.__factid = newid
        
    def get_factid(self):
        return self.__factid
        
    def remove(self):
        '''
        Ritratta una wme dalla Rete
        '''
        # rimuovo questa wme da tutte le alphamemory
        # in cui e' presente
        
        from icse.rete.Nodes import AlphaMemory
        
        for amem in self.__alphamemories:
            assert isinstance(amem, AlphaMemory), \
                "amem non e' AlphaMemory"
            
            amem.remove_wme(self)
            
        # rimuovo tutti i token ottenuti
        # dal confronto con questa wme
        # (insieme ai discendenti in quanti non piu'
        # validi essendo venuta meno una precondizione)
                # la rimozione del token deve essere richiesta dal token
        #for tok in self.__tokens:
        #    tok.delete()
        while len(self.__tokens) > 0:
            tok = self.__tokens[0]
            tok.delete()
            
        for jr in self.__njresults:
            assert isinstance(jr, NegativeJoinResult), \
                "jr non e' una NegativeJoinResult"
                
            jr.get_owner().remove_njresult(jr)
            # eseguo l'attivazione della negative-join
            # se non ci sono altri token
            if jr.get_owner().count_njresults() == 0:
                # bisogna propagare
                for child in jr.get_owner().get_node().get_children():
                    child.leftActivation(jr.get_owner(), None)
        
    def add_token(self, t):
        '''
        Aggiunge un nuovo token alla lista dei riferimenti
        dei tokens in cui questa WME e' rappresentata
        '''
        self.__tokens.insert(0, t)
        
    def remove_token(self, t):
        '''
        Rimuove il riferimento ad un token dalla lista
        dei token in cui questa WME e' rappresentata
        '''
        self.__tokens.remove(t)
        
    def add_alphamemory(self, am):
        self.__alphamemories.insert(0, am)
        
    def remove_alphamemory(self, am):
        self.__alphamemories.remove(am)
        
    def add_njresult(self, njr):
        '''
        Aggiunge una NegativeJoinResult alla lista
        '''
        self.__njresults.insert(0, njr)
        
    def remove_njresult(self, njr):
        '''
        Rimuove una NegativeJoinResult dalla lista
        '''
        self.__njresults.remove(njr)

    def get_field(self, field):
        '''
        Restituisce il valore rappresentato dal field
        @param field: simbol il campo 
        @return: simbol
        '''
        return self.__fields[field]
    
    def get_epoch(self):
        return self.__time
    
    def get_fact(self):
        return self.__fields
    
    def get_length(self):
        return len(self.__fields)
    
    def __hash__(self):
        return hash(tuple(self.__fields))
        
    def __eq__(self, other):
        return ( isinstance(other, WME) and tuple(self.__fields) == tuple(other.__fields))

    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return repr(self.__fields)
