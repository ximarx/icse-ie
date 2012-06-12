'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action
from icse.rete.WME import WME
import icse.debug as debug

class TraceWme(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
    SIGN = 'trace-wme'
    
    def executeImpl(self, *args):
        
        args = self._resolve_args(False, True, *args)
        
        for wme in args:
            if isinstance(wme, WME):
                debug.show_wme_details(wme, explodeToken=True, maxDepth=4, explodeAMem=True)
        
        
    