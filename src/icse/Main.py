'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.Production import Production
from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Variable import Variable
from icse.rete.predicati.Not import Not
from icse.rete.ReteNetwork import ReteNetwork

if __name__ == '__main__':

    # diciamo che vogliamo
    # aggiungere una nuova produzione alla rete
    
    
    # il formato della produzione e':
    # class Production
    #    get_rhs(): [] lista di condizioni
    #    get_lhs(): [] lista di azioni
    
    
    p = Production(name='produzione-di-test',
                   lhs=[
                        # verificata per le wme di tipo (sym p *)
                        [(Eq.__class__, "sym"), (Eq.__class__, "p"), (Variable.__class__, "b") ],
                        # verificata per le wme di tipo (sym c *)
                        [(Eq.__class__, "sym"), (Eq.__class__, "c"), (Variable.__class__, "b") ],
                        # verificata per le wme di tipo (sym a *)
                        [(Eq.__class__, "sym"), (Eq.__class__, "a"), (Not.__class__, (Variable.__class__, "b"))],
                        # verificata per le wme di tipo (sym l *)
                        [(Eq.__class__, "sym"), (Eq.__class__, "l"), (Not.__class__, (Variable.__class__, "b"))],
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
    
    
    
    
    