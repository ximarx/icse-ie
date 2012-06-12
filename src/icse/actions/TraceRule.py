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
    
    def executeImpl(self, *rules):
        rete = self.getReteNetwork()
        pnodes = [rete.get_production(rulename) for rulename in list(rules)]
        debug.draw_network_fragment(pnodes, rete)
        
        
    