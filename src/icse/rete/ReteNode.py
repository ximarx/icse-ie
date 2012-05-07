'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''

class ReteNode(object):
    '''
    Nodo base appartenente alla BetaNetwork (nodo a due input)
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        
        # @ivar __children: [ReteNode] 
        self.__children = []
        self.__parent = parent
        
        
    def leftActivation(self, tok, wme):
        '''
        Attiva il nodo da sinistra (l'attivazione da sinistra corrisponde
        ad un nuovo match proveniente da un nodo ReteNode padre)
        '''
        raise NotImplementedError
    
    def rightActivation(self, wme):
        '''
        Attiva il nodo da destra (l'attivazione da destra corrisponde
        ad un nuovo wme che giunge da un nodo della AlphaNetwork
        '''
        raise NotImplementedError
    
    def delete(self):
        '''
        Esegue le operazioni comuni di pulizia dei nodi
        della BetaNetwork in modo che le classi che estendono
        possono semplicemente chiamare questa funzione
        per eseguire la pulizia base. Esegue:
            - rimozione del riferimento dalla lista di figli del padre
            - rimozione di tutti i nodi sopra questo che non abbiano utilita'
        '''
        self.__parent._remove_child(self)
        self.__parent._delete_useless()
        
    
    def update(self, child):
        '''
        Forza l'attivazione di un nodo appena aggiunto con i risultati
        memorizzati nel nodo
        '''
        raise NotImplementedError
    
    def _remove_child(self, child):
        self.__children.remove(child)
        
    def _delete_useless(self):
        if len(self.__children) == 0:
            self.delete()
            