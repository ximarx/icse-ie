'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.AlphaMemory import AlphaMemory
from icse.rete.Token import Token
from icse.rete.NegativeJoinResult import NegativeJoinResult

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
        
    def remove(self):
        '''
        Ritratta una wme dalla Rete
        '''
        # rimuovo questa wme da tutte le alphamemory
        # in cui e' presente
        for amem in self.__alphamemories:
            assert isinstance(amem, AlphaMemory), \
                "amem non e' AlphaMemory"
            
            amem.remove_wme(self)
            
        # rimuovo tutti i token ottenuti
        # dal confronto con questa wme
        # (insieme ai discendenti in quanti non piu'
        # validi essendo venuta meno una precondizione)
        while len(self.__tokens) > 0:
            tok = self.__tokens.pop(0)
            assert isinstance(tok, Token), \
                "tok non e' un Token"
            tok.delete()   
            
        for jr in self.__njresults:
            assert isinstance(jr, NegativeJoinResult), \
                "jr non e' una NegativeJoinResult"
                
            jr.get_owner().remove_njresult(jr)
        
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
