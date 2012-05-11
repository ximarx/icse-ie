'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.Token import Token
from icse.rete.Nodes import BetaMemory


class PNode(BetaMemory):
    '''
    Nodo terminale di un ReteNetwork
    Rappresenta una produzioneactivable,
    '''


    def __init__(self, parent,
                 # informazioni sulla produzione
                 name,
                 actions,
                 symbols,
                 # triggers
                 onActive=lambda pnode,token:None,
                 onDeactive=lambda pnode,token:None,
                 assertFunc=lambda fact:(None,None,False),
                 retractFunc=lambda wme:None,
                 addProduction=lambda production:None,
                 removeProduction=lambda pnode:None
                ):
        '''
        Constructor
        '''
        self.__onActive = onActive
        self.__onDeactive = onDeactive
        self.__assertFunc = assertFunc
        self.__retractFunc = retractFunc
        self.__addProduction = addProduction
        self.__removeProduction = removeProduction
        
        self.__actions = actions
        self.__name = name
        self.__symbols = symbols

        BetaMemory.__init__(self, parent)
        
    def leftActivation(self, tok, wme=None):
        
        new_token = Token(self, tok, wme)
        self._items.insert(0, new_token)
            
        self.__onActive(self, new_token )
        
    def remove_item(self, tok):
        
        BetaMemory.remove_item(self, tok)
        
        # dopo la rimozione devo anche notificare
        # che l'attivazione non e' piu disponibile
        
        self.__onDeactive(tok)
        
    def get_name(self):
        return self.__name
        
    def factory(self, parent):
        raise NotImplementedError
    
    
    def execute(self, token):
        
        # devo linearizzare il token
        # ed eseguire le azioni
        
        for action in self.__actions:
            #TODO token linearizzato
            action.execute()
        
        
    