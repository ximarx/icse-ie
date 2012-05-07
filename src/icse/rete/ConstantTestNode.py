'''
Created on 07/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.AlphaNode import AlphaNode
from icse.rete.predicati.Predicate import Predicate
from icse.rete.WME import WME
from icse.rete.AlphaMemory import AlphaMemory

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
        
    def activation(self, w):
        '''
        Attivazione del nodo per una nuova wme:
        testa se la condizione e' espressa da questa e' valida
        e nel caso lo sia l'aggiunge alla AlphaMemory collegata
        e propaga ai figli di questo nodo 
        '''
        assert isinstance(w, WME), \
            "w non e' una WME"
        
        predicate = self.__predicate
        assert isinstance(predicate, Predicate)
        
        if predicate.compare(w.get_field(self.__field), self.__value):
            # la wme ha superato il test, quindi e' valida per questa condizione
            
            # se ho una alpha memory collegata a questo test
            #    (e quindi ho dei betanode che derivano da questo)
            #    attivo la alpha memory
            if self.__alphamemory != None:
                assert isinstance(self.__alphamemory, AlphaMemory), \
                    "alphamemory non e' una AlphaMemory"
                self.__alphamemory.activation(w)

            # propago ai figli
            for child in self.__children:
                assert isinstance(child, ConstantTestNode), \
                    "child non e' un ConstantTestNode"
                    
                child.activation(w)
        
    def delete(self):
        '''
        Esegue la rimozione del nodo
        dalla rete
        '''
        #il parent di questo e' per forza un ConstantTestNode
        self.__parent._remove_child(self)
        
        # rimuovo l'eventuale riferimento all'alpha memory
        self.__alphamemory = None
        
    def _remove_child(self, child):
        self.__children.remove(child)
        
        # se no ho altri figli e nemmeno una alphamemory
        # allora questo nodo e' inutile e lo poto
        if len(self.__children) == 0 and self.__alphamemory == None:
            self.delete()
            
        