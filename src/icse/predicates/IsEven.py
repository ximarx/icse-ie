'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Predicate import PositivePredicate

class IsEven(PositivePredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
        
    SIGN = 'evenp'
        
    @staticmethod
    def compare(value1):
        '''
        Restituisce True se value1 e' un numero (float o int)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        # controlla l'ultimo bit :)
        return not (int(value1) & 1)
        
    
        
