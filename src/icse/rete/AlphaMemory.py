'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.AlphaNode import AlphaNode
from icse.rete.ConstantTestNode import ConstantTestNode

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
        # contiene i riferimenti a tutti i nodi successori (nodi beta)
        self.__successors = []

    def get_items(self):
        return self.__items

    @staticmethod
    def factory(c, node):
        '''
        Factory di AlphaMemory:
        costruisce un nuovo nodo AlphaMemory solo se non
        e' possibile utilizzare un nodo gia presente
        condividendolo
        
        @param c: Condition la condizione che rappresenta il nodo
        @param node: AlphaNode il nodo fra i quali figli vogliamo cercare
            un nodo che rappresenti la condizione c in modo da poterlo condividere
        @return: AlphaMemory
        '''
        #TODO riferimento:
        #    build-or-share-alpha-memory(c: condition) pagina 35
        return AlphaMemory()
    
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
        