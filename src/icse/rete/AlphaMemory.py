'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.AlphaNode import AlphaNode
from icse.rete.ConstantTestNode import ConstantTestNode
from icse.rete.RootNode import RootNode
from Queue import Queue

class AlphaMemory(AlphaNode):
    '''
    Nodo AlphaMemory dell'AlphaNetwork
    
    Conserva tutti i riscontri della WM (wme) che hanno 
    matchato condizioni di un ConstantTestNode
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # prepara il parent
        AlphaNode.__init__(self, parent)
        # contiene i riferimenti a tutte le wme
        self.__items = []
        # contiene i riferimenti a tutti i nodi successori (nodi beta [JoinNode])
        self.__successors = []

    def get_items(self):
        '''
        Restituisce la lista di elementi memorizzati
        nella AlphaMemory
        @return: WME[]
        '''
        return self.__items
    
    def add_successor(self, succ):
        '''
        Aggiunge un nuovo elemento nella lista
        dei successori
        @param succ: ReteNode (JoinNode)
        '''
        # aggiungo in testa in modo da evitare la duplicazione
        # di wme evitando di dover fare controlli per evitare
        # la duplicazione.
        # Riferimento:
        #    paragrafo 2.4.1 pagina 25
        self.__successors.insert(0, succ)

    def remove_successor(self, succ):
        '''
        Rimuove il successore dalla lista
        '''
        self.__successors.remove(succ)

    def is_useless(self):
        '''
        Controlla se il nodo puo' essere rimosso:
        il nodo diventa inutile se non ha
        successori
        @return: boolean
        '''
        return (len(self.__successors) == 0)

    @staticmethod
    def factory(node):
    #def factory(c, node):
        '''
        Factory di AlphaMemory:
        costruisce un nuovo nodo AlphaMemory solo se non
        e' possibile utilizzare un nodo gia presente
        condividendolo
        
        #@param c: Condition la condizione che rappresenta il nodo
        @param node: AlphaNode il nodo fra i quali figli vogliamo cercare
            un nodo che rappresenti la condizione c in modo da poterlo condividere
        @return: AlphaMemory
        '''
        #TODO riferimento:
        #    build-or-share-alpha-memory(c: condition) pagina 35
        assert isinstance(node, ConstantTestNode), \
            "node non e' un ConstantTestNode"
            
        if node.has_alphamemory():
            # semplicemente la condivido
            return node.get_alphamemory()
        
        # non c'e' una alphamemory collegata, la creo e l'aggiunto
        am = AlphaMemory(node)
        # provvedo a collegarla ad un test-node
        node.set_alphamemory(am)
        
        # a questo punto devo forzare l'aggiornamento dell'intera rete
        # ora capisco perche il factory aveva come condizione l'intera rete di condizioni...
        
        # ricostruisco semplicemente la sequenza di test node che porta a questa alpha-memory
        stack = []
        tree_cursor = node
        while not isinstance(tree_cursor, RootNode):
            stack.insert(0, tree_cursor)
            tree_cursor = tree_cursor.get_parent()
            
        # tree_cursor e' un RootNode
        assert isinstance(tree_cursor, RootNode)
        
        network = tree_cursor.get_network()
            
        # a questo punto devo testarli tutti per tutte le wme :(
        wmes = network.get_wmes()
        
        for w in wmes:
            isValid = True
            for t in stack:
                assert isinstance(t, ConstantTestNode), \
                    "t no e' un ConstantTestNode"
                
                if not t.is_valid(w):
                    isValid = False
                    break
        
            if isValid:
                # la wme ha passato tutti i test
                # triggo questa alpha-memory come se fosse
                # stata appena aggiunta normalmente
                am.activation(w)
                
        return am
        
    
    def activation(self, w):
        '''
        Esegue l'attivazione della AlphaMemory, memorizzando
        il nuovo elemento WME in memoria e propagandolo
        ai successori
        
        @param w: WME la wme che ha generato l'attivazione
        '''
        
        # riferimento: alpha-memory-activation pagina 32 [modificato]
        
        #assert isinstance(w, WME), \
        #    "w non di tipo WME"
        
        # inserisce il nuovo elemento in testa della lista di elementi
        self.__items.insert(0, w)
        # inserisce questa amem nella lista delle amem di w
        # in modo che realizzare una tree-based removal
        w.add_alphamemory(self)
        
        for succ in self.__successors:
            #assert isinstance(succ, ReteNode), \
            #    "succ non di tipo ReteNode"
            succ.rightActivation(w)
            
        
    def delete(self):
        '''
        Cancella questo nodo
        e propaga la cancellazione al padre se
        il padre non e' condiviso con altri nodi
        '''
        while len(self.__items) > 0:
            item = self.__items.pop(0)
            item.remove_alphamemory(self)
            
        #TODO propagazione al ConstantTestNode a cui si riferisce
        #    questa amem
        #    probabilmente mi servirà un riferimento verso l'alto
        parent = self.get_parent()
        assert isinstance(parent, ConstantTestNode), \
            "parent non e' un ConstantTestNode"
            
        parent.delete() 
        
    def remove_wme(self, w):
        '''
        Rimuove il riferimento alla WME dalla memoria
        
        @param w: WME la wme da rimuove dalla memoria 
        '''
        
        #assert isinstance(w, WME), \
        #    "w non di tipo WME"
        
        self.__items.remove(w)
        