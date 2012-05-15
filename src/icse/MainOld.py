'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.Production import Production
from icse.predicates.Eq import Eq
from icse.Variable import Variable
from icse.rete.ReteNetwork import ReteNetwork
from icse.predicates.Predicate import NccPredicate, PositivePredicate,\
    NegativePredicate, TestPredicate
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper
from icse.predicates.NotEq import NotEq
from icse.predicates.Great import Gt
from icse.functions.Addition import Addition
from icse.Function import Function


if __name__ == '__main__':

    
    rete = ReteNetwork()
    
    '''
    (defrule r1
        (A =(+ 1 1) B)
    =>
    )
    '''
    p = Production(name="r1:",
                   lhs=[
                        (PositivePredicate, [(Eq, 'A'), (Variable, 'var')]),
                        (PositivePredicate, [(Eq, 'A'), (Function.withFunction(Addition), [(Eq, 1), (Variable, 'var')]), (Eq, "B")]),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    rete.assert_fact(['A', 1])
    rete.assert_fact(['A', 2,'B'])
    rete.assert_fact(['A', 1,'B'])
    
    
    agenda = rete.agenda()
    
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())

    NetworkXGraphWrapper.i().draw()    
    
    
    
    
    
    
    
    
    
    
    
    
    