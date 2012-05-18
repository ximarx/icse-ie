'''
Created on 16/mag/2012

@author: Francesco Capozzo
'''
from icse.actions import Action

class Printout(Action):
    '''
    Stampa una lista di simboli su una device
    '''
        
    SIGN = 'printout'
    
    _special_chars = {
            "crlf" : "\n"
        }
    
    @staticmethod
    def _translate_symbol(symbol):
        try:
            return Printout._special_chars[symbol]
        except KeyError:
            import sys
            print >> sys.stderr, \
                "Carattere speciale {{{0}}} non riconosciuto. Verra' interpretato come stringa".format(symbol)
            return symbol
    
    def executeImpl(self, deviceId, *args):
        device = self._devices[deviceId]
        args = [self._translate_symbol(x) if isinstance(x, (str,unicode)) and x[0] != '"' else x for x in list(args)]
        args = self._resolve_args(False, True, *args)
        changed_args = [x[1:-1] if isinstance(x, (str, unicode)) and x[0] == '"' and x[-1] == '"'
                        #else Printout._translate_symbol(x) if isinstance(x, (str, unicode))
                        else str(x) if isinstance(x, (list, dict))
                        else str(x)
                        for x in args]
        
        device.writelines(changed_args)
        
    