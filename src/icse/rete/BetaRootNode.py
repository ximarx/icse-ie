'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.JoinNode import JoinNode

class BetaRootNode(JoinNode):
    '''
    Rappresenta la 
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
        