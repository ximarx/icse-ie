'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import StrategyManager

class Agenda(object):
    '''
    Agenda
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # contiene le attivazioni
        # organizzate come dizionario
        # di lista di attivazioni
        # con indice salience
        self._activations = {}
        # un dizionario di liste di attivazioni di regole
        # indicizzate per nome di regole
        self._fired_activations = {}
        
        self._strategy = StrategyManager.strategy()
        
    def insert(self, pnode, token):
        '''
        Inserisce la nuova attivazione di una regola
        su una sequenza di wmes fra gli attivabili
        e fra quelli in attesa di attivazione
        '''
        from icse.rete.PNode import PNode
        assert isinstance(pnode, PNode)

        salience = pnode.get_property('salience', 0)

        try:
            same_salience_queue = self._activations[salience]
        except KeyError:
            # non c'e' ancora nessuna regola con quella salience
            # non c'e' bisogno di riordino
            self._activations[salience] = [(pnode, token)]
            return
        
        #devo inserire nella posizione giusta nella lista
        self._strategy.insert(pnode, token, same_salience_queue)
    
    def get_activation(self):
        '''
        Restituisce l'attivazione in attesa
        con priorita' massima
        '''
        max_salience = max(self._activations.keys())
        pnode, token = self._activations[max_salience].pop(0)
        if len(self._activations[max_salience]) == 0:
            # rimuove la lista per la salience
            # visto che non ci sono altre regole
            # con quella salience (in questo modo max_salience e' consistente
            del self._activations[max_salience]
            
        
        if self._fired_activations.has_key(pnode.get_name()):
            # uso la lista che gia ho
            fired_per_rule = self._fired_activations[pnode.get_name()]
        else:
            # creo la nuova lista
            # e la inserisco
            fired_per_rule = []
            self._fired_activations[pnode.get_name()] = fired_per_rule
            
        # semplicemente inserisco l'attivazione
        fired_per_rule.append((pnode, token))
        
        return (pnode, token)
        
    def refresh(self, rulename):
        '''
        Resetta tutte le attivazioni di rulename
        con wmes gia attivate
        '''
        try:
            for pnode, token in self._fired_activations[rulename]:
                self.insert(pnode, token)
        except KeyError:
            # la regola non ha attivazioni gia eseguite
            # ignoro la chiamata
            return
        
    def remove(self, pnode, token):
        '''
        Rimuove una attivazione
        dalla lista delle attivazioni
        e degli attivabili
        '''
        salience = pnode.get_property('salience', 0)
        
        try:
            same_salience_queue = self._activations[salience]
            
#            print
#            print "---"
#            print same_salience_queue
#            print pnode.get_name()
#            print token.linearize()
            
            same_salience_queue.remove((pnode, token))
            # se non ci sono altre attivazioni
            # rimuovo
            if len(same_salience_queue) == 0:
                del self._activations[salience]
        except (KeyError, ValueError):
            # non c'e' nessuna attivazione disponibile?
            # allora da dove viene questo token?
            
            # non c'e' questa attivazione nell'agenda
            # suppongo che stia provando a rimuovere
            # l'attivazione della stessa regola che ha
            # attivato l'azione di rimozione
            pass
            
        # una volta rimosso dagli attivabili
        # devo anche prendermi cura delle attivazioni eseguite
        # e ancora eseguibili, rimuovendolo da quella lista
        try:
            self._fired_activations[pnode.get_name()].remove((pnode, token))
        except (KeyError, ValueError):
            pass
            
        
    def clear(self):
        '''
        Resetta completamente lo stato dell'agenda
        (eliminando anche le informazioni
        riguardanti tutti gli elementi che devono ancora
        essere attivati)
        '''
        self._activations = {}
        self._fired_activations = {}

    def refreshAll(self):
        for rulename in self._fired_activations.keys():
            self.refresh(rulename)
    
    def isEmpty(self):
        '''
        Indica se ci sono altre regole in attesa
        di attivazione nella coda o se tutto l'eseguibile
        e' stato eseguito
        '''
        return len(self._activations) == 0
    
    def changeStrategy(self, strategy):
        if self._strategy != strategy:
            self._strategy = strategy
            if not self.isEmpty():
                # devo rioirdinare le attivazioni
                # in base alla nuova strategia
                for per_saliance_list in self._activations.values():
                    self._strategy.resort(per_saliance_list)
                    
    def activations(self):
        saliences = sorted(self._activations.keys(), reverse=True)
        activations = []
        for salience in saliences:
            for (pnode, token) in self._activations[salience]:
                activations.append((salience, pnode, token))
        return activations
    