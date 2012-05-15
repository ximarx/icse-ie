'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Eq import Eq
from icse.predicates.Predicate import NegativePredicate

class NotEq(NegativePredicate):
    '''
    Not condizione
    '''
    
    @staticmethod
    def compare(value1, value2):
        return not Eq.compare(value1, value2)
        