'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.Token import Token
from icse.rete.WME import WME
from icse.rete.predicati.Predicate import Predicate
from icse.rete.predicati.Variable import Variable
from icse.rete.predicati.Eq import Eq

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
        
        assert isinstance(predicate, Predicate), \
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
            
        # il primo elemento da confrontare e' di facile
        # individuazione
        arg1 = wme.get_field(self.__cond1_field)
        
        # individuo il campo di confronto
        # risalendo tanti livelli nell'albero dei token
        # quanti sono i rel_cond_index
        
        t_tok = tok
        i = self.__cond2_rel_index
        while i != 0:
            t_tok = t_tok.get_parent()
            i -= 1
            
        # ora in t_tok ho proprio il token
        # in cui e' rappresentata la wme che mi serve
        wme2 = t_tok.get_wme()
        arg2 = wme2.get_field(self.__cond2_field)
        
        assert isinstance(self.__predicate, Predicate)
        
        return self.__predicate.compare(arg1, arg2)
        
    @staticmethod        
    def build_tests(atoms, prec_conditions, builtins):
        tests = []
        atom_index = 0
        for atom in atoms:
            if isinstance(atom[0], Variable):
                # ho trovato una variabile
                symbol = atom[1]
                if builtins.has_key(symbol):
                    # la variabile l'ho gia trovata prima
                    cond_index, field_index = builtins[symbol]
                    jt = JoinTest(atom_index, field_index, len(prec_conditions) - cond_index, Eq.__class__)
                    tests.append(jt)
            
            atom_index += 1
        return tests
                
        
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
        