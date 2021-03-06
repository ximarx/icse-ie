'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''

import ebnf
import pyparsing as pp
import string
from icse.Function import Function
from icse.Variable import Variable

def _get_function_from_string(funcname):
    import icse.functions as functions
    return functions.Proxy.get(funcname.rstrip())
    
def _get_predicate_from_string(predname):
    import icse.predicates as predicates
    return predicates.Proxy.get(predname.rstrip())

def _get_action_from_string(actionname):
    import icse.actions as actions
    return actions.Proxy.get(actionname.rstrip())

def _get_strategy_from_string(strategyname):
    try:
        if strategyname != 'depth':
            import icse.utils as utils
            strategyname = strategyname.capitalize() + "Strategy"
            return utils.new_object_from_complete_classname("icse.strategies.{0}.{1}".format(strategyname, strategyname))
        else:
            from icse.strategies import DepthStrategy
            return DepthStrategy()
    except Exception, e:
        print e
        import sys
        print >> sys.stderr, "Nome strategia {0} non valido".format(strategyname)
    

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
            from icse.predicates.Eq import Eq
            
            import os
            
            grammar_file = open(os.path.dirname(__file__)+'/clips.ebnf', 'r')
            grammar = grammar_file.read()
            
            table = {}
            table['float'] = pp.Regex(r'\d+(\.\d*)?([eE]\d+)?').setParseAction(lambda s,l,t:float(t[0])) 
            table['integer'] = pp.Word(pp.nums).setParseAction(lambda s,l,t:int(t[0][:]))
            table['string'] = pp.Word(pp.printables)
            table['symbol'] = pp.Word("".join( [ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ] ))
            table['variable_symbol'] = pp.Word('?', "".join( [ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ] ), 2)
            table['variable_undef'] = pp.Literal('?')
            table['quoted_text'] = pp.Combine(("'" + pp.CharsNotIn("'") + "'" ^ \
                                '"' + pp.CharsNotIn('"') + '"'))
            
            import icse.actions as actions
            #table['action_name'] = pp.Combine(pp.oneOf(" ".join(actions.Proxy.get_actions().keys())) + pp.Optional( pp.Literal(" ").suppress()) )
            table['action_name'] = pp.Combine(pp.oneOf(actions.Proxy.get_actions().keys()) + pp.FollowedBy( pp.White() |  pp.Literal(")") ) + pp.Optional( pp.Literal(" ").suppress()) )
            
            import icse.functions as functions
            table['function_name'] = pp.Combine(pp.oneOf(" ".join(functions.Proxy.get_functions().keys())) + pp.Literal(" ").suppress())

            import icse.predicates as predicates
            table['predicate_name'] = pp.Combine(pp.oneOf(" ".join(predicates.Proxy.get_predicates().keys())) + pp.Literal(" ").suppress())
            
            table['MYCLIPS_directive'] =  pp.Regex(r'\;\@(?P<command>\w+)\((?P<params>.+?)\)').setParseAction(lambda s,l,t: ('myclips-directive', (t['command'], t['params'])))
            
            parsers = ebnf.parse(grammar, table, debug)
            
            #parsers['comment'].setParseAction(lambda s,l,t:t[0][1:-1])
            parsers['number'].setParseAction(lambda s,l,t:t[0][0])
            parsers['rule_property'].setParseAction(lambda s,l,t: tuple([t[1], t[2][0]])) 
            parsers['declaration'].setParseAction(lambda s,l,t: ('declare', dict(t[1][:])))
            parsers['comment'].setParseAction(lambda s,l,t: ('description', t[0][1:-1]))
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
            parsers['predicate_name'].setParseAction(lambda s,l,t: _get_predicate_from_string(t[0]) )
            parsers['function_name'].setParseAction(lambda s,l,t: _get_function_from_string(t[0]) )
            # registra la funzione per la function call
            # per provare a riscrivere la funzione come fosse
            # una costante se tutti i termini della funzione sono costanti
            parsers['function_call'].setParseAction(ClipsEbnf._try_rewrite_staticfunction)
            parsers['term_function_call'].setParseAction(lambda s,l,t: t[0] if len(t) == 1 else t[1] )
            parsers['deffacts_name'].setParseAction(lambda s,l,t: ('name', t[0]))
            parsers['rhs_pattern'].setParseAction(lambda s,l,t: [t[1][:]])
            parsers['rhs_pattern_group'].setParseAction(lambda s,l,t: ('facts', t[0][:]))
            parsers['deffacts_construct'].setParseAction(lambda s,l,t: ('deffacts', dict([x for x in t if isinstance(x, tuple)]).get('facts')))
            
            parsers['action_quoted_text'].setParseAction(lambda s,l,t: "".join(t) )
            parsers['action_call'].setParseAction(lambda s,l,t: (t[1],t[2][:]) )
            parsers['action_name'].setParseAction(lambda s,l,t: _get_action_from_string(t[0]) )
            
            parsers['setstrategy_construct'].setParseAction(lambda s,l,t: ('set-strategy', _get_strategy_from_string(t[1]) ))
            
            #parsers['MYCLIPS_directive'].setParseAction(lambda s,l,t: ('myclips-directive', (t[0], t[1][:]) ))
            
            clipsComment = ( ";" + pp.NotAny('@') + pp.SkipTo("\n") ).setName("clips_comment")

            parsers['CLIPS_program'].setParseAction(lambda s,l,t: t[0][:])
            parsers['CLIPS_program'].ignore(clipsComment)
            
        
            if debug:
                # vistualizzo informazioni su funzioni e predicati caricati
                print "Predicati caricati:"
                print "\t" + "\n\t".join(predicates.Proxy.get_predicates().keys())
                print "Funzioni caricate:"
                print "\t" + "\n\t".join(functions.Proxy.get_functions().keys())
                print "Azioni caricate:"
                print "\t" + "\n\t".join(actions.Proxy.get_actions().keys()) 
                raw_input()
                
        
            ClipsEbnf._CACHED_CLIPS_EBNF = parsers
            ClipsEbnf._DEBUG = debug
            
        return ClipsEbnf._CACHED_CLIPS_EBNF['CLIPS_program']          
    
    @staticmethod   
    def _try_rewrite_staticfunction(s,l,t):
        condizioni = t[2][:]
        funcImpl = t[1]
        need_resolution = [ ( issubclass(x, Variable) or issubclass(x, Function)) for (x,_) in condizioni]
        #print condizioni
        #print need_resolution  
        if not True in need_resolution :
            # prima ad eseguire l'operazione direttamente
            from icse.predicates.Eq import Eq
            return (Eq, funcImpl.sign()['handler'](*[x for (_,x) in condizioni]))
        else:
            return (Function.withFunction(t[1]), condizioni)
            
if __name__ == '__main__':
    
    ClipsEbnf.get_parser(True)
    
    test_funct = '''
(set-strategy random)
'''
    
    parsed = ClipsEbnf._CACHED_CLIPS_EBNF['action_group'].parseString(test_funct)[:]
    
    import pprint
    
    pprint.pprint(parsed)
    
            
