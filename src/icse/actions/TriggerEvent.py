'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action
from icse.debug import EventManager

class TriggerEvent(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
    SIGN = 'trigger-event'
    
    def executeImpl(self, triggerName, *args):
        
        args = self._resolve_args(False, True, *args)
        EventManager.trigger(triggerName, args)
        
        
    