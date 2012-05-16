'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Retract(Action):
    '''
    Stampa una lista di simboli su una device
    '''
    SIGN = 'retract'
    
    def executeImpl(self, facts, *args):
        for fact in facts:
            self.retractFact(fact)
        
    