
import ebnf

import pyparsing as pp
import string


def _compile_parser(debug=False):
    
    from icse.rete.predicati.Predicate import PositivePredicate, TestPredicate,\
        NegativePredicate, NccPredicate
    from icse.rete.predicati.NotEq import NotEq
    from icse.rete.predicati.Variable import Variable
    from icse.rete.predicati.Eq import Eq
    from icse.rete.predicati.Great import Gt
    
    
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
    parsers['function_name'].setParseAction(lambda s,l,t: Eq )
    parsers['deffacts_name'].setParseAction(lambda s,l,t: ('name', t[0]))
    parsers['rhs_pattern'].setParseAction(lambda s,l,t: [t[1][:]])
    parsers['rhs_pattern_group'].setParseAction(lambda s,l,t: ('facts', t[0][:]))
    parsers['deffacts_construct'].setParseAction(lambda s,l,t: ('deffacts', dict([x for x in t if isinstance(x, tuple)]).get('facts')))
    parsers['CLIPS_program'].setParseAction(lambda s,l,t: t[0][:])
    
    #print parsers
    return parsers['CLIPS_program']
    


def parse(text, debug=False):
    '''
    Legge una stringa
    '''
    
    parser = _compile_parser(debug)
    
    return parser.parseString(text, True)
    
    
def parseFile(filepath, debug=False):
    
    filer = open(filepath, 'r')
    return parse(filer.read(), debug)
    
    
    
def debug_parsed(items):
    
    for (_, item) in items:
        if isinstance(item, dict):
            for (k,v) in item.items():
                if isinstance(v, dict):
                    print "{0} : {{\n{1}\n}}".format(k,
                                        "\n".join(
                                            ["\t{0} : {1}".format(kk, vv) for (kk,vv) in v.items()]
                                        )
                                    )
                elif isinstance(v, list):
                    print "{0} : [\n\t{1}\n]".format(k,
                                        "\n\t".join([repr(x) for x in v])
                                    )
                else:
                    print "{0} : {1}".format(k, v)
        elif isinstance(item, list):
            for x in item:
                print x
        else:
            print item
    
    
    
    
