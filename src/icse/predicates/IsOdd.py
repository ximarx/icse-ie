'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Predicate import PositivePredicate

class IsOdd(PositivePredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
        
    SIGN = 'oddp'
        
    @staticmethod
    def compare(value1):
        '''
        Restituisce True se value1 e' un numero (float o int)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        return (int(value1) & 1)
        
