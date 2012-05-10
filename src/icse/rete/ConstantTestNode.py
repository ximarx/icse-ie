'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.AlphaNode import AlphaNode
from icse.rete.predicati.Predicate import Predicate


class ConstantTestNode(AlphaNode):
    '''
    Nodo di test inter-condition appartenente all'AlphaNetwork
    '''


    def __init__(self, parent, field, value, predicate):
        '''
        Constructor
        '''
        
        assert isinstance(parent, AlphaNode), \
            "parent non e' un AlphaNode"
            
        assert isinstance(predicate, Predicate), \
            "predicate non e' un Predicate"
        
        AlphaNode.__init__(self, parent)
        
        self.__value = value
        self.__predicate = predicate
        self.__field = field
        
        # list aid figli ConstantTestNode
        self.__children = []
        
        self.__alphamemory = None
        
    def get_predicate(self):
        return self.__predicate
    
    def get_field(self):
        return self.__field
    
    def get_value(self):
        return self.__value
    
    def set_alphamemory(self, amem):
        #assert isinstance(amem, AlphaMemory), \
        #    "amem non e' un AlphaMemory"
            
        self.__alphamemory = amem
        
    def has_alphamemory(self):
        return self.__alphamemory != None
    
    def get_alphamemory(self):
        return self.__alphamemory
        
    @staticmethod
    def factory(node, field, value, predicate):
        '''
        Cerca un ConstantTestNode che e' possibile condividere
        oppure ne crea uno nuovo con le informazioni a disposizione
        e lo inserisce nel Network
        '''
        
        assert isinstance(node, AlphaNode), \
            "node non e' un AlphaNode"
        assert isinstance(predicate, Predicate), \
            "predicate non e' un Predicato"
        
        for child in node.get_parent().get_children():
            # controllo che nn ci sia gia un nodo che mi controlla la stessa cosa
            # se c'e' provvedo semplicemente ad usare quello
            if isinstance(child, ConstantTestNode) \
                and child.get_field() == field \
                and child.get_predicate() == predicate \
                and child.get_value() == value:
                # il nodo di confronto e' lo stesso
                # posso condividerlo
                return child
            
            
        # non abbiamo trovato nessun nodo che verifica le stesse
        # caratteristiche
        
        ctn = ConstantTestNode(node, field, value, predicate)
        node.add_child(ctn)
        
        # il ctn non conserva wme, quindi non devo aggiornarlo
        
        return ctn
        
    def activation(self, w):
        '''
        Attivazione del nodo per una nuova wme:
        testa se la condizione e' espressa da questa e' valida
        e nel caso lo sia l'aggiunge alla AlphaMemory collegata
        e propaga ai figli di questo nodo 
        '''
        #assert isinstance(w, WME), \
            #"w non e' una WME"
        
        if self.is_valid(w):
            # la wme ha superato il test, quindi e' valida per questa condizione
            
            # se ho una alpha memory collegata a questo test
            #    (e quindi ho dei betanode che derivano da questo)
            #    attivo la alpha memory
            if self.has_alphamemory():
                #assert isinstance(self.__alphamemory, AlphaMemory), \
                #    "alphamemory non e' una AlphaMemory"
                self.__alphamemory.activation(w)

            # propago ai figli
            for child in self.__children:
                assert isinstance(child, ConstantTestNode), \
                    "child non e' un ConstantTestNode"
                    
                child.activation(w)
                
    def is_valid(self, w):
        
        predicate = self.__predicate
        assert isinstance(predicate, Predicate.__class__)
        
        return predicate.compare(w.get_field(self.__field), self.__value)
        
    def delete(self):
        '''
        Esegue la rimozione del nodo
        dalla rete
        '''
        #il parent di questo e' per forza un ConstantTestNode
        self.__parent._remove_child(self)
        
        # rimuovo l'eventuale riferimento all'alpha memory
        self.__alphamemory = None
        
    def add_child(self, child):
        '''
        Aggiunge un nuovo figlio alla lista
        '''
        self.__children.insert(0, child)
        
    def _remove_child(self, child):
        self.__children.remove(child)
        
        # se no ho altri figli e nemmeno una alphamemory
        # allora questo nodo e' inutile e lo poto
        if len(self.__children) == 0 and self.__alphamemory == None:
            self.delete()
            
        