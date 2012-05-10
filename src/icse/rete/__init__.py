from icse.rete.predicati.Eq import Eq
from icse.rete.predicati.Not import Not
from icse.rete.predicati.Predicate import NccPredicate, PositivePredicate,\
    NegativePredicate
from icse.rete.Nodes import BetaMemory, AlphaMemory, JoinNode, NegativeNode,\
    NccNode
from icse.rete.JoinTest import JoinTest


def network_factory(alpha_root, parent, conditions, earlier_conditions = None, builtins = None):
    '''
    Crea una sottorete di nodi (appropriati)
    in base alle nuove condizioni (e alle precedenti)
    e le inserisce nella rete. Inoltre, restituisce
    l'ultimo nodo della sottorete
    @return: ReteNode
    '''
    
    # movimento di bacino per evitare che il default
    # sia condiviso fra successive chiamate :)
    if earlier_conditions == None:
        earlier_conditions = []
        
    # lo uso per memorizzare la presenza di variabili
    # gia parsate
    if not isinstance(builtins, dict):
        
        # builtins conterra' un dizionario indicizzato
        # dei risconti di variabile al quale corrispondera'
        # ad ogni variabile
        # una lista di posizioni in cui la variabile
        # e' stata trovata
        # [(cond_index, field_index), (cond_index, field_index)...] 
        builtins = {}
        
    assert isinstance(conditions, list), \
        "conditions non e' una list"

    assert isinstance(earlier_conditions, list), \
        "conditions non e' una list"

    # probabilmente dovro super classare
    # AlphaNode e ReteNode con Node
    #assert isinstance(parent, ReteNode), \
    #    "parent non e' un ReteNode"
    
    # se il padre e' constant-test-node
    #    devo scomporre o condividere le condizioni sui test
    #    fino ad arrivare ad una alpha-memory
    #    alla quale 
    
    
    # quello che ci arriva dalla lhs
    '''
    [
        (PositivePredicate, [(Eq, "sym"), (Eq, "p"), (Variable, "b") ]),
        (PositivePredicate, [(Eq, "sym"), (Eq, "c"), (Variable, "b") ]),
        (NegativePredicate, [(Eq, "sym"), (Eq, "a"), (Not, (Variable, "b"))]),
        (NccPredicate, [
            [(Eq, "sym"), (Eq, "l"), (Not, (Variable, "b"))],
            [(Eq, "sym"), (Eq, "l"), (Not, (Variable, "b"))],
            ),
    ]
    '''

    current_node = parent
    
    # ciclo per ogni condizione separatamente
    for c_type, c in conditions:
        if issubclass(c_type, PositivePredicate):
            # siamo in una condizione positiva
            
            current_node = BetaMemory.factory(current_node)
            tests = JoinTest.build_tests(c, earlier_conditions, builtins)
            amem = AlphaMemory.factory(c, alpha_root)
            JoinNode.factory(current_node, amem, tests)
            
        elif issubclass(c_type, NegativePredicate):
            # siamo in una negazione semplice
            # cioe la negazione di una sola condizione
            
            tests = JoinTest(c, earlier_conditions, builtins)
            amem = AlphaMemory.factory(c, alpha_root)
            current_node = NegativeNode.factory(current_node, amem, tests)
            
        elif issubclass(c_type, NccPredicate):
            # siamo in una ncc
            # cioe la negazione di un insieme di condizioni

            current_node = NccNode.factory(parent, c, earlier_conditions, builtins)
            
        else:
            print "Regola non riconosciuta"
            print  
        
        earlier_conditions.append(c)
        
    return current_node
    
    
    
