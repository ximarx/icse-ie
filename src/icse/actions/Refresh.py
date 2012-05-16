'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Refresh(Action):
    '''
    Stampa una lista di simboli su una device
    '''
    SIGN = 'refresh'
    
    def executeImpl(self, rulenames, *args):
        pass
        
    