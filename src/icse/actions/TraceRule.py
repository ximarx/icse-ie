'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action
import icse.debug as debug

class TraceRule(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
    SIGN = 'trace-rule'
    
    def executeImpl(self, rulename):
        rete = self.getReteNetwork()
        pnode = rete.get_production(rulename)
        debug.draw_network_fragment(pnode)
        
        
    