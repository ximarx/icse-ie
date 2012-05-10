'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.ConstantTestNode import ConstantTestNode

class AlphaRootNode(ConstantTestNode):
    '''
    Finto alpha node che semplicemente propaga qualsiasi segnale ai figli
    '''


    def __init__(self, network):
        '''
        Constructor
        '''
        self.__network = network
        
    def get_network(self):
        return self.__network
        
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
        
        
    