'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.Predicate import PositivePredicate, NumberPredicate

class GreaterThan(PositivePredicate, NumberPredicate):
    '''
    Predicato di maggiore-uguale-di:
        controlla se un valore e' uguale a tutti gli altri forniti
    '''
    
    SIGN = '>'
        
    @staticmethod
    def compare(*args):
        '''
        Restituisce (value1 > tutti gli altri)
        @param value1: numerico
        @param valueN..: numerico 
        @return: boolean
        '''
        try:
            values = NumberPredicate.cast_numbers(*args)
            value1 = values[0]
            for valueN in values[1:]:
                if value1 <= valueN:
                    return False
                
            return True
            
        except:
            return False
    
    

    
                