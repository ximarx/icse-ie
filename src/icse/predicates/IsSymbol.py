'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.predicates.IsString import IsString

class IsSymbol(IsString):
    '''
    Predicato di uguaglianza:
        controlla se un valore e' uguale ad un altro
    '''
    SIGN = 'symbolp'
