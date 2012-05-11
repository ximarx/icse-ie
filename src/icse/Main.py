'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.Production import Production
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Variable import Variable
from icse.rete.predicati.Not import Not
from icse.rete.ReteNetwork import ReteNetwork
from icse.rete.predicati.Predicate import NccPredicate, PositivePredicate,\
    NegativePredicate
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper

if __name__ == '__main__':

    # diciamo che vogliamo
    # aggiungere una nuova produzione alla rete
    
    
    # il formato della produzione e':
    # class Production
    #    get_rhs(): [] lista di condizioni
    #    get_lhs(): [] lista di azioni
    
    
    '''
    (defrule r1
        (A ?v ?v)
        (A ?v B)
    =>
    )
    
    (defrule r2
        (A ?v B)
        (A B ?v)
    =>
    )
    
    (deffacts init-facts
        (A B B)
        (A)
    )    
    '''
    
    rete = ReteNetwork()
    
    p = Production(name="transitivita",
                   lhs=[
                        (PositivePredicate, [(Variable, "A"), (Eq, "per"), (Variable, "B")]),
                        (PositivePredicate, [(Variable, "B"), (Eq, "per"), (Variable, "C")]),
                        (PositivePredicate, [(Variable, "A"), (Eq, "per"), (Variable, "C")])
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)
    
    

    p = Production(name="variabile-interna",
                   lhs=[
                        (PositivePredicate, [(Variable, "A"), (Eq, "uguale"), (Variable, "A")])
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    p = Production(name="variabile-interna-2",
                   lhs=[
                        (PositivePredicate, [(Variable, "zz"), (Eq, "uguale"), (Variable, "wz")]),
                        (PositivePredicate, [(Variable, "wz"), (Eq, "uguale"), (Variable, "wz")])
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)
    
    p = Production(name='produzione-di-test',
                   lhs=[
                        (PositivePredicate, [(Eq, "a"),  (Variable, "v"),  (Variable, "v") ]),
                        (PositivePredicate, [(Eq, "a"),  (Eq, "b"),  (Variable, "v") ])
                        ],
                   rhs=[],
                   description="Una produzione di test"
                   )
    
    # costruiamo la rete
    
    rete.add_production(p)
    
    p2 = Production(name='produzione-di-test-2',
                   lhs=[
                        (PositivePredicate, [(Eq, "a"),  (Variable, "v"),  (Eq, "b") ]),
                        (PositivePredicate, [(Eq, "a"),  (Eq, "b"),  (Variable, "v") ])
                        ],
                   rhs=[],
                   description="Una produzione di test 2"
                   )
 
    rete.add_production(p2)
    

    rete.assert_fact("A per B".split(" "))
    rete.assert_fact("B per Z".split(" "))
    rete.assert_fact("A per Z".split(" "))

    rete.assert_fact("G uguale G".split(" "))
    rete.assert_fact("G uguale R".split(" "))

    rete.assert_fact("G uguale T".split(" "))
    rete.assert_fact("T uguale R".split(" "))
    
    
    

    # dopo di che asseriamo una serie di fatti che dovrebbero
    # permettere un match della produzione
    
    rete.assert_fact( ('a', 'b', 'b') )
    rete.assert_fact( ('a', 'b', 'c') )
    rete.assert_fact( ('a', 'c', 'b') )
    
    rete.assert_fact( ('a') )
    
    NetworkXGraphWrapper.i().draw()    
    
    agenda = rete.agenda()
    
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())
    
    
    
    