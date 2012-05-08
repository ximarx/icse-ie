'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.ConstantTestNode import ConstantTestNode

class RootNode(ConstantTestNode):
    '''
    Finto alpha node che semplicemente propaga qualsiasi segnale ai figli
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def get_parent(self):
        return self
    
    def activation(self, w):
        for child in self.__children:
            assert isinstance(child, ConstantTestNode), \
                "child non e' un ConstantTestNode"
            child.activation(w)
        
    def delete(self):
        '''
        Niente da fare
        '''
        
        
    