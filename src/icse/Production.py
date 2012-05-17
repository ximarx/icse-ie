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


    def __init__(self, name, lhs, rhs, properties=None, description=None):
        '''
        Constructor
        '''
        self.__name = str(name)
        self.__rhs = rhs
        self.__lhs = lhs
        if properties == None:
            properties = {'salience':0}
        self.__properties = properties
        self.__description = str(description)
        
        if not properties.has_key('specificity'):
            properties['specificity'] = self._calcolate_specificity(lhs)
        
    def get_name(self):
        return self.__name
        
    def get_rhs(self):
        return self.__rhs
        
    def get_lhs(self):
        return self.__lhs
    
    def get_properties(self):
        return self.__properties
    
    def _calcolate_specificity(self, lhs):
        from icse.predicates.Predicate import PositivePredicate, NegativePredicate, NccPredicate, TestPredicate  
        from icse.predicates.Eq import Eq
        from icse.predicates.NotEq import NotEq
        from icse.Variable import Variable
        from icse.Function import Function
        
        specificity = 0
        for (predicate, args) in lhs:
            if issubclass(predicate, (PositivePredicate, NegativePredicate)):
                for (arg_type, arg_value) in args:
                    if issubclass(arg_type, (Eq, NotEq, Variable)):
                        specificity += 1
                    elif issubclass(arg_type, Function):
                        # controllo dentro gli argomenti, ma solo
                        # per 1 ricorsione
                        # e quindi ignorero tutti gli elementi
                        # non Eq,NotEq,Variable
                        specificity += 1
                        for (sub_arg_type, _) in arg_value:
                            if issubclass(sub_arg_type, (Eq, NotEq, Variable)):
                                specificity += 1
            elif issubclass(predicate, (NccPredicate, TestPredicate)):
                for sub_predicate in args:
                    if issubclass(sub_predicate, (PositivePredicate, NegativePredicate)):
                        for (arg_type, arg_value) in args:
                            if issubclass(arg_type, (Eq, NotEq, Variable)):
                                specificity += 1
                            elif issubclass(arg_type, Function):
                                # controllo dentro gli argomenti, ma solo
                                # per 1 ricorsione
                                # e quindi ignorero tutti gli elementi
                                # non Eq,NotEq,Variable
                                specificity += 1
                                for (sub_arg_type, _) in arg_value:
                                    if issubclass(sub_arg_type, (Eq, NotEq, Variable)):
                                        specificity += 1
                
            
            
        return specificity
        