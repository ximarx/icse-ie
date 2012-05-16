'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Assert(Action):
    '''
    Stampa una lista di simboli su una device
    '''
    SIGN = 'assert'
    
    def executeImpl(self, facts, *args):
        for fact in facts:
            self.assertFact(fact)
        
    