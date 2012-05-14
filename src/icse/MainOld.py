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
        ((A uno) (B due))
    =>
    )    
    '''
    p = Production(name="r1:",
                   lhs=[
                        (PositivePredicate, {'_': (Eq, 'template_id'), 'A': (Eq, "uno"), 'B': (Variable, "due")}),
                        ],
                   rhs=[],
                   description=""
                   )
    
    rete.add_production(p)


    rete.assert_fact({
                      '_': 'template_id',
                      'A': 'uno',
                      'B': 'due'
                      })
    
    
    agenda = rete.agenda()
    
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())

    NetworkXGraphWrapper.i().draw()    
    
    
    
    
    
    
    
    
    
    
    
    
    