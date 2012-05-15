'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.Token import Token, DummyToken
from icse.rete.WME import WME
from icse.predicates.Predicate import Predicate, TestPredicate
from icse.Variable import Variable
from icse.predicates.Eq import Eq


class FilterTest(object):
    '''
    JoinTest: rappresenta un test di coerenza per il binding
    di variabili in condizioni differenti rappresentati
    da un JoinNode
    '''


    def __init__(self, field1_rel_index, field1, field2_rel_index, field2, predicate):
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
        self.__cond1_rel_index = field1_rel_index
        self.__cond2_rel_index = field2_rel_index
        self.__predicate = predicate
        
        
    def perform(self, tok):
        '''
        Esegue un controllo di coerenza per il binding
        delle variabili rappresentate da questa classe
        '''
        
        # Riferimento: perform-join-tests pagina 25
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        # Il confronto deve avvenire necessariamente
        # fra variabili bindate precedentemente
        # quindi direttamente 

        wme1 = None
        wme2 = None

        # risolvo l'atomo primario
        
        if self.__cond1_rel_index != None:
            t_tok = tok
            i = self.__cond1_rel_index - 1
            while i > 0:
                t_tok = t_tok.get_parent()
                i -= 1
                
            # ora in t_tok ho proprio il token
            # in cui e' rappresentata la wme che mi serve
            wme1 = t_tok.get_wme()


        if self.__cond2_rel_index != None:
            t_tok = tok
            i = self.__cond2_rel_index - 1
            while i > 0:
                t_tok = t_tok.get_parent()
                i -= 1
                
            # ora in t_tok ho proprio il token
            # in cui e' rappresentata la wme che mi serve
            wme2 = t_tok.get_wme()

        
        try:
            
            # se ho una wme, allora il campo e' un indice di campo
            # altrimenti e' proprio il valore
            if wme1 == None:
                arg1 = self.__cond1_field
            else:
                arg1 = wme1.get_field(self.__cond1_field)
            
            # se ho una wme, allora il campo e' un indice di campo
            # altrimenti e' proprio il valore
            if wme2 == None:
                arg2 = self.__cond2_field
            else:
                arg2 = wme2.get_field(self.__cond2_field)
            
            assert issubclass(self.__predicate, Predicate)
            
            #print arg1, ' VS ',arg2
            
            return self.__predicate.compare(arg1, arg2)
        except IndexError:
            # Il confronto non e' nemmeno necessario
            # visto che una delle wme non ha nemmeno
            # il numero di campi richiesto per il confronto
            return False
        
    @staticmethod        
    def build_tests(atoms, prec_conditions, builtins, predicate):
        tests = []
        atom_index = 0
        first_atom = None
        for atom_type, atom_value in atoms:
        
            # il primo atomo e' il confronto di tutti
            if issubclass(atom_type, Variable):
                # devo risolverla
                cond_index, cond_field = builtins[atom_value]
                # eseguo aggiustamento relativo
                cond_index = len(prec_conditions) - cond_index
            else:
                # e' un valore reale di confronto
                cond_index = None
                cond_field = atom_value
            
            if first_atom == None:
                # salvo il primo valore
                # che sia O:
                #    - indice relativo di condizione, indice di campo dove risiede il valore
                #    - None, il valore
                first_atom = (cond_index, cond_field)
            else:
                # creo il test fra:
                #     il primo valore/variabile
                # VS
                #     il corrente valore/variabile
                ft = FilterTest(first_atom[0], first_atom[1], cond_index, cond_field, predicate)
                tests.append(ft)
                # non aggiorno la builtins
                # in quanto non voglio che le future funzioni
                # cerchino con un valore errato
                # in quanto questo test non crea token
            
            atom_index += 1
            
        #print [repr(x) for x in tests]
        
        return tests
             
        
    def __repr__(self):
        if self.__cond2_rel_index != None:
            s2 = "[{0}] di {1}".format(
                                   self.__cond2_field,
                                   self.__cond2_rel_index * -1
                                   )
        else:
            s2 = self.__cond2_field
            
        if self.__cond1_rel_index != None:
            s1 = "[{0}] di {1}".format(
                                   self.__cond1_field,
                                   self.__cond1_rel_index * -1
                                   )
        else:
            s1 = self.__cond1_field 

        return "{0} {1} {2}".format(
                                s1,
                                self.__predicate.SIGN if hasattr(self.__predicate, 'SIGN') and self.__predicate.SIGN != None else str(self.__predicate.__name__).split('.')[-1],
                                s2
                            )
        
    def __eq__(self, other):
        if isinstance(other, FilterTest):
            if self.__cond1_field == other.__cond1_field \
                and self.__cond2_field == other.__cond2_field \
                and self.__cond1_rel_index == other.__cond1_rel_index \
                and self.__cond2_rel_index == other.__cond2_rel_index \
                and self.__predicate == other.__predicate:
                
                return True
            
        return False
        
    def __neq__(self, other):
        return (not self.__eq__(other))
        
    def __hash__(self):
        # speriamo mi faciliti il confronto fra liste di test...
        return hash((self.__cond1_field, self.__cond2_field, self.__cond1_rel_index, self.__cond2_rel_index, self.__predicate))
        