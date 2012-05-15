'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Predicate import NegativePredicate

class StringNotEq(NegativePredicate):
    '''
    Predicato di disuguaglianza:
        controlla se un valore e' diverso da tutti gli altri (almeno uno)
    '''
        
    SIGN = 'neq'
        
    @staticmethod
    def compare(*args):
        '''
        Restituisce (value1 != tutti gli altri)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        if len(args) == 2:
            value1, value2 = args
            return (value1 != value2)
        else:
            value1 = args[0]
            for altro in list(args[1:]):
                if value1 == altro:
                    return False
                
            return True 
            
        