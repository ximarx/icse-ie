'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''

class NegativeJoinResult(object):
    '''
    Match di un join negativo
    '''


    def __init__(self, owner, wme):
        '''
        Constructor
        '''
        
        #assert isinstance(owner, Token), \
        #    "owner non e' un Token"
            
        #assert isinstance(wme, WME), \
        #    "wme non e' un WME"
        
        self.__owner = owner
        self.__wme = wme
        
    
    def get_owner(self):
        '''
        Restituisce il token nella cui memoria locale risiede il risultato
        @return: Token 
        '''
        return self.__owner
    
    def get_wme(self):
        '''
        Restituisce la wme che matcha il token
        @return: WME
        '''
        return self.__wme
    
