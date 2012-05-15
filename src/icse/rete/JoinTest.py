'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.Token import Token, DummyToken
from icse.rete.WME import WME
from icse.predicates.Predicate import Predicate
from icse.Variable import Variable
from icse.predicates.Eq import Eq
from icse.Function import Function

class JoinTest(object):
    '''
    JoinTest: rappresenta un test di coerenza per il binding
    di variabili in condizioni differenti rappresentati
    da un JoinNode
    '''


    def __init__(self, field1, field2, rel_cond_index, predicate):
        '''
        Costruisce un nuovo JoinTest
        @param field1: il tipo di campo da confrontrare di prima WME
        @param field2: il tipo di campo da confrontrare di seconda WME
        @param rel_cond_index: indice relativo del token a cui appartiene la WME da confrontare
        @param predicate: il predicato che eseguira' il confronto 
        '''
        
        assert issubclass(predicate, Predicate), \
            "predicate non e' un Predicate"
        
        self.__cond1_field = field1
        self.__cond2_field = field2
        self.__cond2_rel_index = rel_cond_index
        self.__predicate = predicate
        
        
    def perform(self, tok, wme):
        '''
        Esegue un controllo di coerenza per il binding
        delle variabili rappresentate da questa classe
        '''
        
        # Riferimento: perform-join-tests pagina 25
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        if self.__cond2_rel_index > 0:
            # cerco fra i token precedenti

            t_tok = tok
            i = self.__cond2_rel_index - 1
            while i > 0:
                t_tok = t_tok.get_parent()
                i -= 1
                
            # ora in t_tok ho proprio il token
            # in cui e' rappresentata la wme che mi serve
            wme2 = t_tok.get_wme()
        
        else:
            # il confronto e' sulla
            # stessa wme
            wme2 = wme
        
        # individuo il campo di confronto
        # risalendo tanti livelli nell'albero dei token
        # quanti sono i rel_cond_index
        
        try:
            
            # il primo elemento da confrontare e' di facile
            # individuazione
            arg1 = wme.get_field(self.__cond1_field)
            
            arg2 = wme2.get_field(self.__cond2_field)
            
            assert issubclass(self.__predicate, Predicate)
            
            return self.__predicate.compare(arg1, arg2)
        except IndexError:
            # Il confronto non e' nemmeno necessario
            # visto che una delle wme non ha nemmeno
            # il numero di campi richiesto per il confronto
            return False
        
    @staticmethod        
    def build_tests(atoms, prec_conditions, builtins):
        tests = []
        #atom_index = 0
        tmp_atoms = atoms.keys() if isinstance(atoms, dict) else range(0, len(atoms))
        for key in tmp_atoms:
            atom = atoms[key]
            atom_index = key
            if issubclass(atom[0], Variable):
                # ho trovato una variabile
                symbol = atom[1]
                if symbol != None:
                    if builtins.has_key(symbol):
                        # la variabile l'ho gia trovata prima
                        cond_index, field_index = builtins[symbol]
                        jt = JoinTest(atom_index, field_index, len(prec_conditions) - cond_index, atom[0].get_predicate())
                        tests.append(jt)
                    else:
                        builtins[symbol] = (len(prec_conditions), atom_index)
            elif issubclass(atom[0], Function):
                # devo importare un tipo di join speciale
                # che sia in grado di valutarmi
                # la funzione
                
                # considerazioni:
                # se negli argomenti di funzione
                # non appaiono variabili, la funzione puo
                # anche essere valutata staticamente e convertita
                # in un constant-test-node
                # ma questo lavoro dovrebbe gia essere stato fatto
                # al momento del parsing della regola
                # in modo da velocizzare la compilazione
                
                # quindi sono certo che negli argomenti della funzione sia
                # presente ALMENO una variabile
                # ed inoltre la variabile DEVE essere stata gia dichiarata prima
                
                dynop = DynamicOperand(atom[0].get_function(), atom[1], len(prec_conditions), builtins)
                
                fjt = FunctionJoinTest(atom_index, dynop)
                tests.append(fjt)
                
                
            
            #atom_index += 1
            
        #print [("["+str(x.__cond2_field)+"] di -"+str(x.__cond2_rel_index), x.__predicate, "["+ str(x.__cond1_field)+"]") for x in tests]
        
        return tests
             
    def __repr__(self):
        return "[{0}] di {1} {2} [{3}]".format(
                                         str(self.__cond2_field),
                                         str(self.__cond2_rel_index * -1),
                                         self.__predicate.SIGN if hasattr(self.__predicate, 'SIGN') and self.__predicate.SIGN != None else str(self.__predicate.__name__).split('.')[-1],
                                         str(self.__cond1_field)
                                         )
        
    def __eq__(self, other):
        if isinstance(other, JoinTest):
            if self.__cond1_field == other.__cond1_field \
                and self.__cond2_field == other.__cond2_field \
                and self.__cond2_rel_index == other.__cond2_rel_index \
                and self.__predicate == other.__predicate:
                
                return True
            
        return False
        
    def __neq__(self, other):
        return (not self.__eq__(other))
        
    def __hash__(self):
        # speriamo mi faciliti il confronto fra liste di test...
        return hash((self.__cond1_field, self.__cond2_field, self.__cond2_rel_index, self.__predicate))
    
    
    
class FunctionJoinTest(JoinTest):
    
    def __init__(self, field_index, dynoperand):
        self._field_index = field_index
        self._dynop = dynoperand
        
    
    def perform(self, tok, wme):
        return (wme.get_field(self._field_index) == self._dynop.valutate(tok, wme))
    
    
    def __repr__(self):
        return "{0} = [{1}]".format(
                                    repr(self._dynop),
                                    str(self._field_index)
                                )
    
    
    
class DynamicOperand(object):
    
    def __init__(self, funccls, operands, prec_cond_count, builtins):
        
        import icse.functions as fnc
        
        assert issubclass(funccls, fnc.Function ), \
            "funccls non e' un fnc.Function"
            
        self._function = funccls
        
        self._operands = []
        
        for (op_type, op_value) in operands: 
            if issubclass(op_type, Variable):
                cond_index, field_index = builtins[op_value] 
                self._operands.append( (prec_cond_count - cond_index, field_index) )
            elif issubclass(op_type, Function):
                # ricorsione
                self._operands.append(DynamicOperand(op_type.get_function(), op_value, prec_cond_count, builtins))
            else:
                self._operands.append(op_value)
                
    def valutate(self, token, wme, builtins_refs = None):
        if builtins_refs == None:
            builtins_refs = {}
        
        #risolvo realmente le variabili
        return self._function.sign()['handler'](*[
                                  x.valutate(token, wme, builtins_refs) if isinstance(x, DynamicOperand) \
                                    else self._resolve_variable(x[0], x[1], token, wme, builtins_refs) if isinstance(x, tuple) \
                                    else x 
                                  for x in self._operands  
                                ])
        
    def _resolve_variable(self, y, x, tok, wme, builtins_refs):
        # metto le variabili gia risolte all'interno
        # di un dizionario per non doverle risolvere
        # nuovamente
        
        dict_key = (y,x)
        
        if builtins_refs.has_key(dict_key):
            return builtins_refs[dict_key]
        
        
        if y > 0:
            # cerco fra i token precedenti

            t_tok = tok
            i = y - 1
            while i > 0:
                t_tok = t_tok.get_parent()
                i -= 1
                
            # ora in t_tok ho proprio il token
            # in cui e' rappresentata la wme che mi serve
            wme_var = t_tok.get_wme()
        
        else:
            # il confronto e' sulla
            # stessa wme
            # che e' impossibile..... ma non si sa mai
            wme_var = wme
        
        value = wme_var.get_field(x)
        
        builtins_refs[dict_key] = value
        return value
        
    def __repr__(self,):
        return "({0}: {1})".format(
                                self._function.sign()['sign'] \
                                    if hasattr(self._function, 'sign') \
                                        and isinstance(self._function.sign(), dict) \
                                        and self._function.sign().has_key('sign') \
                                    else str(self._function.__name__).split('.')[-1],
                                ", ".join([ 
                                        repr(x) \
                                            if isinstance(x, DynamicOperand) \
                                            else "[{0}] di {1}".format(
                                                                    x[1], x[0] * -1           
                                                            ) \
                                                if isinstance(x, tuple) \
                                                else str(x)
                                        for x in self._operands
                                    ])
                        ) 
        
        