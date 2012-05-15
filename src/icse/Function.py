'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function as FuncLogicBase

class Function(object):
    '''
    Indica una variabile
    '''

    _function = None
    _function_variance = {}

        
    @staticmethod
    def withFunction(p):
        '''
        Costruisce a runtime una nuova sottoclasse di 
        variable che matcha con un predicato differente
        (e memorizza, in modo da riutilizzarlo per
        altre richieste con lo stesso predicato)
        '''
        assert issubclass(p, FuncLogicBase)
        
        newclassname = "Function_dynamic_"+p.__name__.split('.')[-1]
        
        if not Function._function_variance.has_key(newclassname):
            newclass = type(newclassname, (Function,), {
                                                        '_function' : p,
                                                        })
            Function._function_variance[newclassname] = newclass
        
        return Function._function_variance[newclassname]
        
    @classmethod
    def get_function(cls):
        return cls._function
    