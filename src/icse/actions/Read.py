'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Read(Action):
    '''
    Stampa una lista di simboli su una device
    '''
    SIGN = 'read'
    
    def executeImpl(self, *args):
        return raw_input() 
        
    