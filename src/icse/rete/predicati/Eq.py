'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.predicati.Predicate import PositivePredicate

class Eq(PositivePredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
        
    @staticmethod
    def compare(value1, value2):
        '''
        Restituisce (value1==value2)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        return (value1 == value2)
        