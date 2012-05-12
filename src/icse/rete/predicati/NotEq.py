'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Predicate import NegativePredicate

class NotEq(NegativePredicate):
    '''
    Not condizione
    '''
    
    @staticmethod
    def compare(value1, value2):
        return not Eq.compare(value1, value2)
        