'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class SetStrategy(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
    SIGN = 'set-strategy'
    
    @staticmethod
    def _get_strategy(strategyName):
        import icse.utils as utils
        strategyname = strategyName.capitalize() + "Strategy"
        return utils.new_object_from_complete_classname("icse.strategies.{0}.{1}".format(strategyname, strategyname))
    
    def executeImpl(self, strategyName, *args):
        try:
            strategy = self.__class__._get_strategy(strategyName)
        except KeyError:
            import sys
            print >> sys.stderr, "Strategia {0} non valida".format(strategyName)
            return
        
        self.getReteNetwork().agenda().changeStrategy(strategy)
        
    