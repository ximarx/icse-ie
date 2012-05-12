'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.Production import Production
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Variable import Variable
from icse.rete.ReteNetwork import ReteNetwork
from icse.rete.predicati.Predicate import NccPredicate, PositivePredicate,\
    NegativePredicate, TestPredicate
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper
from icse.rete.predicati.NotEq import NotEq
from icse.rete.predicati.Great import Gt


if __name__ == '__main__':

    
    rete = ReteNetwork()
    
    '''
    (defrule r1
        (A ?ap ?ap)
        (A ?bp ?bp)
        (test (<> ?ap ?bp))
    =>
    )    
    '''
    p = Production(name="r1: A?a?a & A?b?b & ?a<>?b",
                   lhs=[
                        (PositivePredicate, [(Eq, "A"), (Variable, "ap"), (Variable, "ap")]),
                        (PositivePredicate, [(Eq, "A"), (Variable, "bp"), (Variable, "bp")]),
                        (TestPredicate.withPredicate(NotEq), [(Variable, "ap"), (Variable, "bp") ]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)
    

    '''
    (defrule r2
        (A ?a ?a)
    =>
    )
    '''
    p = Production(name="r2: A?a?a",
                   lhs=[
                        (PositivePredicate, [(Eq, "A"), (Variable, "a"), (Variable, "a")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r3
        (A)
    =>
    )
    '''
    p = Production(name="r3: A",
                   lhs=[
                        (PositivePredicate, [(Eq, "A")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r4
        (~A)
    =>
    )
    '''
    p = Production(name="r4: not-A",
                   lhs=[
                        (PositivePredicate, [(NotEq, "A")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    '''
    (defrule r5
        (?a ~?a ?b)
    =>
    )
    '''
    p = Production(name="r5: ?a ~?a ?b",
                   lhs=[
                        (PositivePredicate, [(Variable, "a"), (Variable.withPredicate(NotEq), "a"), (Variable, "b") ]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)

    '''
    (defrule r6
        (A ?a ?b)
        (test (> ?a ?b))
        (B ?a ?b)
    =>
    )
    '''
    p = Production(name="r6: A?a?b && ?a > ?b",
                   lhs=[
                        (PositivePredicate, [(Eq, 'A'), (Variable, "a"), (Variable, "b") ]),
                        (TestPredicate.withPredicate(Gt), [(Variable, "a"), (Variable, "b") ]),
                        (PositivePredicate, [(Eq, 'B'), (Variable, "a"), (Variable, "b") ]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)

    rete.assert_fact("A 2 1".split(" "))
    rete.assert_fact("A 1 1".split(" "))
    rete.assert_fact("A 2 2".split(" "))
    rete.assert_fact("A 1 2".split(" "))
    rete.assert_fact("B 2 1".split(" "))
    rete.assert_fact("B 2 2".split(" "))
    rete.assert_fact("A 2 1 5".split(" "))
    rete.assert_fact("A A Z".split(" "))
    rete.assert_fact("A".split(" "))
    rete.assert_fact("E".split(" "))
    
    
    agenda = rete.agenda()
    
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())

    NetworkXGraphWrapper.i().draw()    
    
    
    
    
    
    
    
    
    
    
    
    
    