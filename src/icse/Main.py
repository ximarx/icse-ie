'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.Production import Production
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Variable import Variable
from icse.rete.ReteNetwork import ReteNetwork
from icse.rete.predicati.Predicate import NccPredicate, PositivePredicate,\
    NegativePredicate
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper
from icse.rete.predicati.NotEq import NotEq


if __name__ == '__main__':

    
    rete = ReteNetwork()
    
    '''
    (defrule r3
        (A ?ap ?ap)
        (A ?bp ?bp)
        (test (neq ?ap ?bp))
    =>
    )    
    '''
    p = Production(name="r3",
                   lhs=[
                        (PositivePredicate, [(Eq, "A"), (Variable, "ap"), (Variable, "ap")]),
                        (PositivePredicate, [(Eq, "A"), (Variable, "bp"), (Variable, "bp")])
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)
    

    '''
    (defrule r4
        (A ?a ?a)
    =>
    )
    '''
    p = Production(name="r4",
                   lhs=[
                        (PositivePredicate, [(Eq, "A"), (Variable, "ap"), (Variable, "ap")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r5
        (A)
    =>
    )
    '''
    p = Production(name="r5",
                   lhs=[
                        (PositivePredicate, [(Eq, "A")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r6
        (~A)
    =>
    )
    '''
    p = Production(name="r6",
                   lhs=[
                        (PositivePredicate, [(NotEq, "A")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r7
        (?a ~?a ?b)
    =>
    )
    '''
    p = Production(name="r7",
                   lhs=[
                        (PositivePredicate, [(Variable, "a"), (Variable.withPredicate(NotEq), "a"), (Variable, "b") ]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)

    print Variable._variable_variance

    
    rete.assert_fact("A 1 1".split(" "))
    rete.assert_fact("A 2 2".split(" "))
    rete.assert_fact("A 1 2".split(" "))
    rete.assert_fact("A A Z".split(" "))
    rete.assert_fact("A".split(" "))
    rete.assert_fact("E".split(" "))
    
    agenda = rete.agenda()
    
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())

    NetworkXGraphWrapper.i().draw()    
    
    
    
    
    