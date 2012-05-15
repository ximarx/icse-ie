'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''

import ebnf
import pyparsing as pp
import string

def _get_function_from_string(funcname):
    pass
    
def _get_predicate_from_string(predname):
    import icse.predicates as predicates
    return predicates.Proxy.get(predname)


class ClipsEbnf(object):
    _CACHED_CLIPS_EBNF = None
    _DEBUG = False
    @staticmethod
    def get_parser(debug=True):
        # se non e' inizializzato
        # oppure se e' richiesto un parser
        # con stato debug diverso dall'attuale
        # lo (ri)compilo
        if ClipsEbnf._CACHED_CLIPS_EBNF == None \
            or debug != ClipsEbnf._DEBUG:
            
            from icse.predicates.Predicate import PositivePredicate, TestPredicate,\
                NegativePredicate, NccPredicate
            from icse.predicates.NotEq import NotEq
            from icse.predicates.Variable import Variable
            from icse.predicates.Eq import Eq
            
            import os
            
            grammar_file = open(os.path.dirname(__file__)+'/clips.ebnf', 'r')
            grammar = grammar_file.read()
            
            table = {}
            table['float'] = pp.Regex(r'\d+(\.\d*)?([eE]\d+)?').setParseAction(lambda s,l,t:float(t[0])) 
            table['integer'] = pp.Word(pp.nums).setParseAction(lambda s,l,t:int(t[0][:]))
            table['string'] = pp.Word(pp.alphas, pp.alphanums)
            table['symbol'] = pp.Word("".join( [ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ] ))
            table['variable_symbol'] = pp.Word('?', pp.alphanums, 2)
            table['variable_undef'] = pp.Literal('?')
            table['quoted_text'] = ("'" + pp.CharsNotIn("'") + "'" ^ \
                                '"' + pp.CharsNotIn('"') + '"')
            
            
            parsers = ebnf.parse(grammar, table, debug)
            
            #parsers['comment'].setParseAction(lambda s,l,t:t[0][1:-1])
            parsers['number'].setParseAction(lambda s,l,t:t[0][0])
            parsers['rule_property'].setParseAction(lambda s,l,t: tuple([t[1], t[2][0]])) 
            parsers['declaration'].setParseAction(lambda s,l,t: ('declare', dict(t[1][:])))
            parsers['comment'].setParseAction(lambda s,l,t: ('description', t[1]))
            parsers['rule_name'].setParseAction(lambda s,l,t: ('name', t[0]))
            parsers['conditional_element_group'].setParseAction(lambda s,l,t: ('lhs', t[0][:]))
            parsers['action_group'].setParseAction(lambda s,l,t: ('rhs', t[0][:]))
            parsers['defrule_construct'].setParseAction(lambda s,l,t: ('defrule', dict([x for x in t if isinstance(x, tuple)])))
            parsers['constant'].setParseAction(lambda s,l,t:(Eq, t[0]))
            parsers['variable_symbol'].setParseAction(lambda s,l,t:(Variable, t[0][1:]))
            parsers['variable_undef'].setParseAction(lambda s,l,t:(Variable, None))
            parsers['pattern_CE'].setParseAction(lambda s,l,t:(PositivePredicate, t[1][:]))
            parsers['not_term'].setParseAction(lambda s,l,t:(NotEq, t[1][1]) if t[1][0] == Eq else (Variable.withPredicate(NotEq), t[1][1]) if t[1][0] == Variable else (NotEq, t[1]) )
            parsers['test_CE'].setParseAction(lambda s,l,t:(TestPredicate.withPredicate(t[2]), t[3][:]))
            parsers['assigned_pattern_CE'].setParseAction(lambda s,l,t:(PositivePredicate, t[2][1][:], t[0][1]))
            parsers['and_CE'].setParseAction(lambda s,l,t: [t[1][:]] )
            parsers['not_CE'].setParseAction(lambda s,l,t: (NegativePredicate, t[1][1]) if t[1][0] == PositivePredicate else (NccPredicate, t[1]))
            parsers['function_name'].setParseAction(lambda s,l,t: _get_predicate_from_string(t[0]) )
            parsers['deffacts_name'].setParseAction(lambda s,l,t: ('name', t[0]))
            parsers['rhs_pattern'].setParseAction(lambda s,l,t: [t[1][:]])
            parsers['rhs_pattern_group'].setParseAction(lambda s,l,t: ('facts', t[0][:]))
            parsers['deffacts_construct'].setParseAction(lambda s,l,t: ('deffacts', dict([x for x in t if isinstance(x, tuple)]).get('facts')))
            parsers['CLIPS_program'].setParseAction(lambda s,l,t: t[0][:])
        
            if debug:
                # vistualizzo informazioni su funzioni e predicati caricati
                import icse.predicates as preds
                print "Predicati caricati:"
                print "\t" + "\n\t".join(preds.Proxy.get_predicates().keys())
                import icse.functions as funcs
                print "Funzioni caricate:"
                print "\t" + "\n\t".join(funcs.Proxy.get_functions().keys())
                raw_input()
                
        
            ClipsEbnf._CACHED_CLIPS_EBNF = parsers
            ClipsEbnf._DEBUG = debug
            
        return ClipsEbnf._CACHED_CLIPS_EBNF['CLIPS_program']          
            
            
