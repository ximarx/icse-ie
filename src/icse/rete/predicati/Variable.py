'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Predicate import Predicate

class Variable(object):
    '''
    Indica una variabile
    '''

    _predicate = Eq
    _variable_variance = {}

        
    @staticmethod
    def withPredicate(p):
        '''
        Costruisce a runtime una nuova sottoclasse di 
        variable che matcha con un predicato differente
        (e memorizza, in modo da riutilizzarlo per
        altre richieste con lo stesso predicato)
        '''
        assert issubclass(p, Predicate)
        
        newclassname = "Variable_dynamic_"+p.__name__.split('.')[-1]
        
        if not Variable._variable_variance.has_key(newclassname):
            newclass = type(newclassname, (Variable,), {
                                                        '_predicate' : p,
                                                        })
            Variable._variable_variance[newclassname] = newclass
        
        return Variable._variable_variance[newclassname]
        
    @classmethod
    def get_predicate(cls):
        return cls._predicate
    