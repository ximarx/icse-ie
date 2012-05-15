'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Predicate import PositivePredicate

class NumberEq(PositivePredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale a tutti gli altri (almeno uno)
    '''
        
    SIGN = '='
        
    @staticmethod
    def compare(*args):
        '''
        Restituisce (value1 == tutti gli altri)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        value1 = args[0]
        if not isinstance(value1, (int, float)): return False
        for altro in list(args[1:]):
            # fallisce se un elemento non e' un numero
            # o se e' diverso dal primo
            if not isinstance(altro, (int, float)) \
                or value1 != altro:
                return False
            
        return True 
            
        