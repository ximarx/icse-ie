'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.predicati.Predicate import PositivePredicate, NumberPredicate

class Gt(PositivePredicate, NumberPredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
        
    @staticmethod
    def compare(value1, value2):
        '''
        Restituisce (value1>value2)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        try:
            nvalue1, nvalue2 = NumberPredicate.cast_numbers(value1, value2)
            return (nvalue1 > nvalue2)
        except:
            return False
    
    
class Ge(PositivePredicate, NumberPredicate):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
        
    @staticmethod
    def compare(value1, value2):
        '''
        Restituisce (value1>=value2)
        @param value1: simbolo
        @param value2: simbolo 
        @return: boolean
        '''
        try:
            nvalue1, nvalue2 = NumberPredicate.cast_numbers(value1, value2)
            return (nvalue1 >= nvalue2)
        except:
            return False
    
    
                