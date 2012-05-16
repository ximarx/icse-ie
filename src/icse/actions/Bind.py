'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action
from icse.Variable import Variable

class Bind(Action):
    '''
    Stampa una lista di simboli su una device
    '''
    SIGN = 'bind'
    
    def executeImpl(self, vartuple, *args):
        if not isinstance(vartuple, tuple) or not issubclass(vartuple[0], Variable):
            raise TypeError("Bind: atteso primo valore Variabile.\n\t(bind ?nome-variabile [valori]+)")
        
        _,varname = vartuple
        args = self._resolve_args(False, True, *args)
        
        # controllo la lunghezza:
        # se len(args) == 1, allora semplicemente salvo il valore

        # CONTROLLARE CHE SUCCEDE CON LE TUPLE DI UNA        
        if len(args) == 1:
            args = args[0]
        
        #pprint.pprint(*args)
        #raise Exception()
        self._symbols[varname] = args
        
    