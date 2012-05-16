'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Printout(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
        
    @staticmethod
    def get_ebnf():
        return '''
        '''
        
    @staticmethod
    def parse_action():
        return ('action_printout', Printout._parse_action_impl)
    
    @staticmethod
    def _parse_action_impl(s,l,t):
        return t
    

    def executeImpl(self, deviceId, *args):
        
        pass
        
    