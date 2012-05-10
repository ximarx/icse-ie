'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''

class Predicate(object):
    '''
    Classe base per l'implementazioni di tutti i predicati
    '''

    @staticmethod
    def compare(self, value1, value2):
        '''
        Esegue la comparazione fra due valori
        secondo le specifiche del predicato
        @param value1: primo valore da confrontare
        @param value2: secondo valore da confrontare al primo
        @return: boolean
        '''
        raise NotImplementedError
    
    
class PositivePredicate(Predicate):
    '''
    Classe base di tutti i predicati positivi
    '''

class NegativePredicate(Predicate):
    '''
    Classe base di tutti i predicati negativi
    '''

class NccPredicate(Predicate):
    '''
    Rappresenta una sottorete di predicati negativi
    '''
