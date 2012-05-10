from icse.rete.ReteNode import ReteNode
from icse.rete.BetaMemory import BetaMemory
from icse.rete.predicati.PositivePredicate import PositivePredicate
from icse.rete.ConstantTestNode import ConstantTestNode
from icse.rete.predicati.Variable import Variable
from icse.rete.AlphaMemory import AlphaMemory
from icse.rete.JoinTest import JoinTest
from icse.rete.predicati.Eq import Eq
from icse.rete.JoinNode import JoinNode


def network_factory(parent, conditions, earlier_conditions = None, builtins = None):
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
        [(Eq.__class__, "sym"), (Eq.__class__, "p"), (Variable.__class__, "b") ],
        [(Eq.__class__, "sym"), (Eq.__class__, "c"), (Variable.__class__, "b") ],
        [(Eq.__class__, "sym"), (Eq.__class__, "a"), (Not.__class__, (Variable.__class__, "b"))],
        [(Eq.__class__, "sym"), (Eq.__class__, "l"), (Not.__class__, (Variable.__class__, "b"))],
    ]
    '''

    current_node = parent
    bottom_prec_condition = None
    
    # ciclo per ogni condizione separatamente
    cond_index = 0 
    for c in conditions:
        # ciclo per ogni elemento di una condizione
        field_index = 0
        for sb in c:
            predicate = sb[0]
            op = sb[1]
        
            # valuto il tipo del predicato
            if issubclass(predicate, PositivePredicate):
                # devo creare il ConstantTestNode
                current_node = ConstantTestNode.factory(current_node, field_index, op, predicate)
                
            elif issubclass(predicate, Variable):
                # devo controllare se e' una nuova variabile
                # se lo e' semplicemente creo una joinnode finta
                if builtins.has_key(op):
                    # la variabile c'e' gia... 
                    # ho bisogno di una join per linkarla
                    # all'altra presenza
                
                    # ultima corrispondenza
                    where = builtins[op][-1]
                    
                    # construisco il test
                    tests = [JoinTest(field_index, where[1], cond_index - where[0], Eq.__class__)]
                    
                    # devo valutare il dove l'ho trovata
                    # se e' nella stessa condizione, allora posso anche risolvere il tutto con una
                    # join-finta
                    if where[0] == cond_index:
                        ''
                    else:
                        # condizione differente, devo costruire una join-vera
                        # per prima cosa mi serve un alpha-memory
                        # per questo sotto albero di costant-test-node
                        
                        am = AlphaMemory.factory(current_node)
                        
                        # a questo punto ho una vista su tutte le wme
                        # che soddisfano le condizioni
                        # fino a questo punto (am)
                        
                        # mi serve sapere la parte sinistra della join
                        # il join deve essere collegato alla fine della porzione
                        # del network ottenuto dalla precedente condizione
                        jn = JoinNode.factory(bottom_prec_condition, am, tests)
                        
                        assert isinstance(bottom_prec_condition, ReteNode), \
                            "bottom_prec_condition non e' un ReteNode"
                        
                        # a questo punto devo impostare l'ultimo nodo come un
                        current_node = jn
                    
                
                else:
                    # prima volta che trovo questa variabile
                    # la memorizzo nella lista di variabili
                    builtins[op] = [(cond_index, field_index)] 
                
                    # inoltre visto che c'e' una variabile, so gia
                    # che mi servira' una alpha-memory con un relativo
                    # join-node (falso... senza ingresso da sinistra)
                    
                    #am = AlphaMemory.factory(current_node)
                    
                    #assert isinstance(current_node, ConstantTestNode), \
                        #"current_node non e' un ConstantTestNode"
                        
                    #current_node.set_alphamemory(am)
                    
                    #RETTIFICA:
                    # fino a quando non mi serve per davvero
                    # non aggiungo proprio nessun memory.node
                    
                
            field_index +=1
        cond_index += 1
        
    
    
    
