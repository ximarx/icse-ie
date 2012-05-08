from icse.rete.ReteNode import ReteNode
from icse.rete.BetaMemory import BetaMemory


def network_factory(parent, conditions, earlier_conditions = None):
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
        
    assert isinstance(conditions, list), \
        "conditions non e' una list"

    assert isinstance(earlier_conditions, list), \
        "conditions non e' una list"

    # probabilmente dovro super classare
    # AlphaNode e ReteNode con Node
    #assert isinstance(parent, ReteNode), \
    #    "parent non e' un ReteNode"
    
    current_node = parent
    
        
            
        
    
    
    
