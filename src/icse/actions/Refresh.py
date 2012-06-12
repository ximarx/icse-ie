'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action
from icse.rete.Agenda import Agenda

class Refresh(Action):
    '''
    Esegue il refresh di una regola
    muovendo tutte le attivazioni gia
    eseguite e ancora valide nuovamente
    nell'agenda
    '''
    SIGN = 'refresh'
    
    def executeImpl(self, rulename, *args):
        agenda = self.getReteNetwork().agenda()
        assert isinstance(agenda, Agenda)
        agenda.refresh(rulename)
        
    