'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''

class AlphaNode(object):
    '''
    Interfaccia per nodi base della AlphaNetwork
    '''
    
    def __init__(self, parent):
        assert isinstance(parent, AlphaNode), \
            "parent non e' AlphaNode"
        self.__parent = parent
        
    def get_parent(self):
        return self.__parent
    
    def activation(self, w):
        '''
        Attivazione del nodo
        @param w: WME la WME che ha provocato l'attivazione 
        '''
        raise NotImplementedError()
    
    def delete(self):
        '''
        Gestisce la cancellazione del nodo
        '''
        raise NotImplementedError()

