'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''

class Production(object):
    '''
    Una produzione (o meglio una regola) in un sistema di produzione:
    la parte sinistra (lhs) contiene la lista di condizioni da valutare
    e verificare affinche la parte destra (rhs), che rappresenta una serie
    di azioni, possa essere eseguita
    '''


    def __init__(self, name, lhs, rhs, salience=0, description=None):
        '''
        Constructor
        '''
        self.__name = str(name)
        self.__rhs = rhs
        self.__lhs = lhs
        self.__salience = salience
        self.__description = str(description)
        
    def get_name(self):
        return self.__name
        
    def get_rhs(self):
        return self.__rhs
        
    def get_lhs(self):
        return self.__lhs