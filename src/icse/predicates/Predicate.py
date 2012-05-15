'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''

class Predicate(object):
    '''
    Classe base per l'implementazioni di tutti i predicati
    '''
    
    '''
    Overloading per inserire il simbolo che corrisponda al predicato
    '''
    SIGN = None

    @staticmethod
    def compare(*args):
        '''
        Esegue la comparazione fra due valori
        secondo le specifiche del predicato
        @param value1: primo valore da confrontare
        @param value2: secondo valore da confrontare al primo
        @return: boolean
        '''
        raise NotImplementedError
    
    
    @classmethod
    def sign(cls):
        return {
                'sign': cls.SIGN,
                'handler': cls.compare,
                'cls': cls
            }    
    
    
class PositivePredicate(Predicate):
    '''
    Classe base di tutti i predicati positivi
    '''

class NegativePredicate(Predicate):
    '''
    Classe base di tutti i predicati negativi
    '''

class NccPredicate(Predicate):
    '''
    Rappresenta una sottorete di predicati negativi
    '''

class TestPredicate(Predicate):
    
    _predicate = None
    _variable_variance = {}
    
    @staticmethod
    def withPredicate(p):
        '''
        Costruisce a runtime una nuova sottoclasse di 
        variable che matcha con un predicato differente
        (e memorizza, in modo da riutilizzarlo per
        altre richieste con lo stesso predicato)
        '''
        #print p
        assert issubclass(p, Predicate), \
            "p non e' un Predicate: "+p.__name__
        
        newclassname = "Variable_dynamic_"+p.__name__.split('.')[-1]
        
        if not TestPredicate._variable_variance.has_key(newclassname):
            newclass = type(newclassname, (TestPredicate,), {
                                                        '_predicate' : p,
                                                        })
            TestPredicate._variable_variance[newclassname] = newclass
        
        return TestPredicate._variable_variance[newclassname]
        
    @classmethod
    def get_predicate(cls):
        return cls._predicate
        
    

class NumberPredicate(Predicate):
    '''
    Richiede che gli operandi siano
    numerici
    '''
    
    @staticmethod
    def cast_numbers(*args):
        return [NumberPredicate._try_cast(x) for x in list(args)]
    
    @staticmethod
    def cast_couple(arg1, arg2):
        return tuple(NumberPredicate.cast_numbers(arg1, arg2))
            
    @staticmethod    
    def _try_cast(value):
        try:
            return int(value)
        except ValueError:
            return float(value)
        
        