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

if __name__ == '__main__':

    # diciamo che vogliamo
    # aggiungere una nuova produzione alla rete
    
    
    # il formato della produzione e':
    # class Production
    #    get_rhs(): [] lista di condizioni
    #    get_lhs(): [] lista di azioni
    
    
    p = Production(name='produzione-di-test',
                   lhs=[
                        (PositivePredicate, [(Eq, "sym"), (Eq, "p"), (Variable, "b") ]),
                        (PositivePredicate, [(Eq, "sym"), (Eq, "c"), (Variable, "b") ]),
                        (NegativePredicate, [(Eq, "sym"), (Eq, "a"), (Not, (Variable, "b"))]),
                        (NccPredicate, [
                                [(Eq, "sym"), (Eq, "l"), (Not, (Variable, "b"))],
                                [(Eq, "sym"), (Eq, "l"), (Not, (Variable, "b"))],
                            ]),
                        ],
                   rhs=[],
                   description="Una produzione di test"
                   )
    
    # costruiamo la rete
    
    rete = ReteNetwork()
    
    rete.add_production(p)

    # dopo di che asseriamo una serie di fatti che dovrebbero
    # permettere un match della produzione
    
    rete.assert_fact( ('sym', 'p', 'vicino') )
    rete.assert_fact( ('sym', 'c', 'vicino') )
    rete.assert_fact( ('sym', 'a', 'lontano') )
    rete.assert_fact( ('sym', 'l', 'lontano') )
    
    
    
    
    