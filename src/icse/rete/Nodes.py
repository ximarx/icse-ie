'''
Created on 10/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.predicati.Predicate import Predicate
from icse.rete.Token import Token, DummyToken
from icse.rete.WME import WME
from icse.rete.predicati.Variable import Variable
from icse.rete.JoinTest import JoinTest
from icse.rete.NegativeJoinResult import NegativeJoinResult

class AlphaNode(object):
    '''
    Interfaccia per nodi base della AlphaNetwork
    '''
    
    def __init__(self, parent):
        #assert isinstance(parent, AlphaNode), \
        #    "parent non e' AlphaNode"
        self._parent = parent
        
    def get_parent(self):
        return self._parent
    
    def activation(self, w):
        '''
        Attivazione del nodo
        @param w: WME la WME che ha provocato l'attivazione 
        '''
        raise NotImplementedError()
    
    def delete(self):
        '''
        Gestisce la cancellazione del nodo
        '''
        raise NotImplementedError()



class ConstantTestNode(AlphaNode):
    '''
    Nodo di test inter-condition appartenente all'AlphaNetwork
    '''


    def __init__(self, parent, field, value, predicate):
        '''
        Constructor
        '''
        
        #assert isinstance(parent, AlphaNode), \
        #    "parent non e' un AlphaNode"
            
        #assert isinstance(predicate, Predicate), \
        #    "predicate non e' un Predicate"
        
        AlphaNode.__init__(self, parent)
        
        self._value = value
        self._predicate = predicate
        self._field = field
        
        # list aid figli ConstantTestNode
        self._children = []
        
        self._alphamemory = None
        
    def get_predicate(self):
        return self._predicate
    
    def get_children(self):
        return self._children
    
    def get_field(self):
        return self._field
    
    def get_value(self):
        return self._value
    
    def set_alphamemory(self, amem):
        #assert isinstance(amem, AlphaMemory), \
        #    "amem non e' un AlphaMemory"
            
        self._alphamemory = amem
        
    def has_alphamemory(self):
        return self._alphamemory != None
    
    def get_alphamemory(self):
        return self._alphamemory
        
    @staticmethod
    def factory(node, field, value, predicate):
        '''
        Cerca un ConstantTestNode che e' possibile condividere
        oppure ne crea uno nuovo con le informazioni a disposizione
        e lo inserisce nel Network
        '''
        
        assert isinstance(node, AlphaNode), \
            "node non e' un AlphaNode"
        assert issubclass(predicate, Predicate), \
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
                #assert isinstance(self._alphamemory, AlphaMemory), \
                #    "alphamemory non e' una AlphaMemory"
                self._alphamemory.activation(w)

            # propago ai figli
            for child in self._children:
                assert isinstance(child, ConstantTestNode), \
                    "child non e' un ConstantTestNode"
                    
                child.activation(w)
                
    def is_valid(self, w):
        
        predicate = self._predicate
        assert isinstance(predicate, Predicate.__class__)
        
        return predicate.compare(w.get_field(self._field), self._value)
        
    def delete(self):
        '''
        Esegue la rimozione del nodo
        dalla rete
        '''
        #il parent di questo e' per forza un ConstantTestNode
        self._parent._remove_child(self)
        
        # rimuovo l'eventuale riferimento all'alpha memory
        self._alphamemory = None
        
    def add_child(self, child):
        '''
        Aggiunge un nuovo figlio alla lista
        '''
        self._children.insert(0, child)
        
    def _remove_child(self, child):
        self._children.remove(child)
        
        # se no ho altri figli e nemmeno una alphamemory
        # allora questo nodo e' inutile e lo poto
        if len(self._children) == 0 and self._alphamemory == None:
            self.delete()
            
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
        self._items = []
        # contiene i riferimenti a tutti i nodi successori (nodi beta [JoinNode])
        self._successors = []

    def get_items(self):
        '''
        Restituisce la lista di elementi memorizzati
        nella AlphaMemory
        @return: WME[]
        '''
        return self._items
    
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
        self._successors.insert(0, succ)

    def remove_successor(self, succ):
        '''
        Rimuove il successore dalla lista
        '''
        self._successors.remove(succ)

    def is_useless(self):
        '''
        Controlla se il nodo puo' essere rimosso:
        il nodo diventa inutile se non ha
        successori
        @return: boolean
        '''
        return (len(self._successors) == 0)

    @staticmethod
    def factory(c, node):
        '''
        Factory di AlphaMemory:
        costruisce un nuovo nodo AlphaMemory solo se non
        e' possibile utilizzare un nodo gia presente
        condividendolo
        
        @param c: la condizione che rappresenta il nodo (espressa come lista di atomi [condizioni su singoli campi])
        @param node: la radice della alpha-network
        @return: AlphaMemory
        '''
        #TODO riferimento:
        #    build-or-share-alpha-memory(c: condition) pagina 35

        for field_index, (atom_type, atom_cont) in enumerate(c):
            if not issubclass(atom_type, Variable):
                # filtra tutte le variabili
                node = ConstantTestNode.factory(node, field_index, atom_cont, atom_type)
                
        # al termine del ramo di valutazione costante, l'ultimo nodo ha gia una
        # alpha-memory: condividiamo quella
        if node.has_alphamemory():
            return node.get_alphamemory()
        
        # altrimenti ne aggiungiamo una nuova
        am = AlphaMemory(node)
        # provvedo a collegarla ad un test-node
        node.set_alphamemory(am)
        
        # a questo punto devo forzare l'aggiornamento dell'intera rete
        # ora capisco perche il factory aveva come condizione l'intera rete di condizioni...
        
        # ricostruisco semplicemente la sequenza di test node che porta a questa alpha-memory
        stack = []
        tree_cursor = node
        while not isinstance(tree_cursor, AlphaRootNode):
            stack.insert(0, tree_cursor)
            tree_cursor = tree_cursor.get_parent()
            
        # tree_cursor e' un RootNode
        assert isinstance(tree_cursor, AlphaRootNode)
        
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
        self._items.insert(0, w)
        # inserisce questa amem nella lista delle amem di w
        # in modo che realizzare una tree-based removal
        w.add_alphamemory(self)
        
        for succ in self._successors:
            #assert isinstance(succ, ReteNode), \
            #    "succ non di tipo ReteNode"
            succ.rightActivation(w)
            
        
    def delete(self):
        '''
        Cancella questo nodo
        e propaga la cancellazione al padre se
        il padre non e' condiviso con altri nodi
        '''
        while len(self._items) > 0:
            item = self._items.pop(0)
            item.remove_alphamemory(self)
            
        #TODO propagazione al ConstantTestNode a cui si riferisce
        #    questa amem
        #    probabilmente mi servira' un riferimento verso l'alto
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
        
        self._items.remove(w)
                    
            
class AlphaRootNode(ConstantTestNode):
    '''
    Finto alpha node che semplicemente propaga qualsiasi segnale ai figli
    '''

    def __init__(self, network):
        '''
        Constructor
        '''
        self._network = network
        ConstantTestNode.__init__(self, None, None, None, None)
        self.set_alphamemory(AlphaMemory(None))
        
    def get_network(self):
        return self._network
        
    def get_parent(self):
        return self
    
    def activation(self, w):
        for child in self._children:
            assert isinstance(child, ConstantTestNode), \
                "child non e' un ConstantTestNode"
            child.activation(w)
        
    def delete(self):
        '''
        Niente da fare
        '''
        


        
class ReteNode(object):
    '''
    Nodo base appartenente alla BetaNetwork (nodo a due input)
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        #assert isinstance(parent, ReteNode), \
        #    "parent non e' un ReteNode"
        
        # @ivar __children: [ReteNode] 
        self._children = []
        self._parent = parent
        
        
    def get_children(self):
        '''
        Getter per children
        '''
        return self._children
    
    def add_child(self, child):
        assert isinstance(child, ReteNode), \
            "child non e' un ReteNode"
            
        self._children.insert(0, child)
        
    def append_child(self, child):
        '''
        Aggiunge il figlio nella lista in ultima posizione
        '''
        assert isinstance(child, ReteNode), \
            "child non e' un ReteNode"
            
        self._children.append(child)
        
    def leftActivation(self, tok, wme):
        '''
        Attiva il nodo da sinistra (l'attivazione da sinistra corrisponde
        ad un nuovo match proveniente da un nodo ReteNode padre)
        '''
        raise NotImplementedError
    
    def rightActivation(self, wme):
        '''
        Attiva il nodo da destra (l'attivazione da destra corrisponde
        ad un nuovo wme che giunge da un nodo della AlphaNetwork
        '''
        raise NotImplementedError
    
    def delete(self):
        '''
        Esegue le operazioni comuni di pulizia dei nodi
        della BetaNetwork in modo che le classi che estendono
        possono semplicemente chiamare questa funzione
        per eseguire la pulizia base. Esegue:
            - rimozione del riferimento dalla lista di figli del padre
            - rimozione di tutti i nodi sopra questo che non abbiano utilita'
        '''
        self._parent._remove_child(self)
        self._parent._delete_useless()
        
    
    def update(self, child):
        '''
        Forza l'attivazione di un nodo appena aggiunto con i risultati
        memorizzati nel nodo
        '''
        raise NotImplementedError
    
    def _remove_child(self, child):
        self._children.remove(child)
        
    def _delete_useless(self):
        if len(self._children) == 0:
            self.delete()
                    
                    
                    
class JoinNode(ReteNode):
    '''
    JoinNode: rappresenta un nodo giunzione fra uno
    proveniente dall'AlphaNetwork e uno proveniente da
    BetaNetwork 
    '''

    def __init__(self, parent, amem, tests):
        '''
        Constructor
        '''

        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"
        
        self._amem = amem
        
        # filtra tutti gli elementi non JoinTest
        self._tests = [x for x in tests if isinstance(x, JoinTest)]
        ReteNode.__init__(self, parent)
        
    
    def leftActivation(self, tok, wme = None):
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        for w in self._amem.get_items():
            if self._perform_tests(w, tok):
                for child in self._children:
                    assert isinstance(child, ReteNode), \
                        "child non e' un ReteNode"
                    
                    # attiva a sinistra i figli
                    # (che sono betamemory o riconducibili)
                    child.leftActivation(tok, w)
    
    def rightActivation(self, wme):
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        assert isinstance(self._parent, BetaMemory), \
            "parent non e' un BetaMemory"
            
        for tok in self._parent.get_items():
            
            if self._perform_tests(wme, tok):
                for child in self._children:
                    assert isinstance(child, ReteNode), \
                        "child non e' un ReteNode"
                    
                    # attiva a sinistra i figli
                    # (che sono betamemory o riconducibili)
                    
                    child.leftActivation(tok, wme)
        

    def _perform_tests(self, wme, tok):
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        assert isinstance(tok, Token), \
            "tok non e' un Token"
        
        for t in self._tests:
            
            if not t.perform(tok, wme):
                return False
        
        return True
    
    @staticmethod
    def factory(parent, amem, tests):

        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"

        for child in parent.get_children():
            # escludo che un join node possa essere condiviso da un
            # NegativeNode con gli stessi test e alpha-memory
            if isinstance(child, JoinNode) and not isinstance(child, NegativeNode):
                #assert isinstance(child, JoinNode)
                if child._amem == amem:
                    if child.__tests == tests:
                        # stessi test, testa amem... condivido il nodo
                        return child
                
        # non posso condividere un nuovo gia esistente
        # con queste informazioni, quindi ne creo uno nuovo
        # e lo aggiunto alla rete
        
        jn = JoinNode(parent, amem, tests)
        parent.add_child(jn)
        amem.add_successor(jn)
        
        return jn
        
    def delete(self):
        '''
        Esegue la cancellazione del nodo
        propagando la cancellazione all'alpha-memory
        se non e' condivisa con altri nodi
        '''
        
        self._amem.remove_successor(self)
        
        if self._amem.is_useless():
            self._amem.delete()
        
        
        ReteNode.delete(self)
        
    def update(self, child):
        
        # memorizzo temporaneamente la lista
        # attuale di figli
        saved_children = self.get_children()
        
        self._children = [child]
        
        for wme in self._amem.get_items():
            assert isinstance(wme, WME), \
                "wme non e' un WME"
            
            # forzo l'aggiornamento di ogni wme che
            # verra' propagata ai figli (che in questo
            # caso sono solo quello nuovo... temporaneamente)    
            self.rightActivation(wme)
            
        # ho aggiornato il figlio, a questo punto
        # ripristino la vecchia lista
        
        self._children = saved_children
        
                            
                            
class BetaMemory(ReteNode):
    '''
    Beta Memory node: contiene la lista di token che matchano un particolare
    insieme di condizioni con intra-riferimenti di variabili
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        ReteNode.__init__(self, parent)
        
        # lista di token mantenuti nella beta memory
        self._items = []
        
    def get_items(self):
        return self._items
    
    def remove_item(self, tok):
        '''
        Rimuove un token dagli items
        '''
        self._items.remove(tok)
    
    def leftActivation(self, tok, wme):
        
        new_token = Token(self, tok, wme)
        self._items.insert(0, new_token)
        
        for child in self._children:
            assert isinstance(child, ReteNode), \
                "child non e' un ReteNode"
                
            # attenzione, la leftActivation viene fornita senza la WME
            # quindi solo i join node sono preparati a riceverla?????
            # TODO refactoring
            child.leftActivation(tok)
            
        
    def delete(self):
        '''
        Cancella tutti i token memorizzati in questo nodo (e chiaramente i successori)
        '''
        
        while len(self._items) > 0:
            tok = self._items.pop(0)
            assert isinstance(tok, Token), \
                "tok non e' un Token"
                
            tok.delete()
            
        # chiama il metodo della classe base
        # per eseguire le operazioni di pulizia
        # comuni a tutti i nodi della BetaNetwork
        ReteNode.delete(self)
        
    def update(self, child):
        
        assert isinstance(child, ReteNode), \
            "child non e' un ReteNode"
        
        for tok in self._items:
            self.leftActivation(tok)
        
    @staticmethod
    def factory(parent):
        
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
            
        for child in parent.get_children():
            if isinstance(child, BetaMemory):
                # semplicemente un beta memory node
                # e un contenitore senza condizioni:
                # cio che discrimina il contenuto e'
                # il join-node padre.
                # quindi se ho gia un nodo betamemory
                # figlio dello stesso padre, semplicemente
                # lo condivido
                return child
        
        # non ho trovato nessun beta-memory
        # figlio del padre, quindi ne aggiungo
        # uno nuovo
        
        bm = BetaMemory(parent)
        parent.add_child(bm)
        parent.update(bm)

        return bm
    
    
class NegativeNode(JoinNode):
    '''
    JoinNode per condizioni negative
    '''


    def __init__(self, parent, amem, tests):
        '''
        Constructor
        '''
        
        # lista di Token
        self._items = []
        
        # amem e tests dal JoinNode come proprieta' "protette"
        # self._amem
        # self._tests
        JoinNode.__init__(self, parent, amem, tests)
        
    def get_items(self):
        '''
        Restituisce la lista di match (come fosse una beta-memory)
        @return: Token[]
        '''
        return self._items
    
    def remove_item(self, tok):
        '''
        Rimuove un token dagli items
        '''
        self._items.remove(tok)
    
        
    @staticmethod
    def factory(parent, amem, tests):
        
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
        assert isinstance(amem, AlphaMemory), \
            "amem non e' una AlphaMemory"
        assert isinstance(tests, list), \
            "tests non e' una list"

        for child in parent.get_children():
            if  isinstance(child, NegativeNode):
                #assert isinstance(child, JoinNode)
                if child._amem == amem:
                    if child.__tests == tests:
                        # stessi test, testa amem... condivido il nodo
                        return child
                
        # non posso condividere un nuovo gia esistente
        # con queste informazioni, quindi ne creo uno nuovo
        # e lo aggiunto alla rete
        
        njn = NegativeNode(parent, amem, tests)
        parent.add_child(njn)
        amem.add_successor(njn)
        
        # aggiorna
        parent.update(njn)
        
        return njn

    def leftActivation(self, tok, wme):

        assert isinstance(wme, WME), \
            "wme non e' un WME"
        
        new_token = Token(self, tok, wme)
        
        self._items.insert(0, new_token)
        
        for w in self._amem.get_items():
            if self._perform_tests(w, new_token):
                njr = NegativeJoinResult(new_token, w)
                
                new_token.add_njresult(njr)
                wme.add_njresult(njr)
                
        # attiva solo se non ci sono match (e' un nodo negativo)
        if new_token.count_njresults() == 0 :
            for child in self._children:
                assert isinstance(child, ReteNode), \
                    "child non e' un ReteNode"
                    
                # attenzione, la leftActivation viene fornita senza la WME
                # quindi solo i join node sono preparati a riceverla?????
                # TODO refactoring
                child.leftActivation(new_token)
        
        
    def rightActivation(self, wme):
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        for t in self._items:
            assert isinstance(t, Token), \
                "t non e' un Token"
                
            if self._perform_tests(wme, t):
                # controllo se prima c'erano match
                if t.count_njresults() == 0:
                    # se non c'erano match
                    # allora il token e' stato propagato
                    # e quindi devo revocarlo
                    t.deleteDescendents()

                # creo il NegativeJoinResult
                njr = NegativeJoinResult(t, wme)
                
                t.add_njresult(njr)
                wme.add_njresult(njr)
    
    def update(self, child):
        '''
        Esegue l'aggiornamento dei figli (attivandoli a sinistra)
        se vengono trovati token che non hanno match per njresult
        (il nodo e' negativo)
        '''
        for t in self._items:
            assert isinstance(t, Token), \
                "t non e' un Token"
                
            if t.count_njresults() == 0:
                child.leftActivation(t)

    def delete(self):
        '''
        Esegue la rimozione del nodo dalla rete,
        pulendo la memoria interna del nodo
        '''
        
        # questo codice e' identico
        # a quello per la pulizia della BetaMemory
        # ma questo elemento non e' derivato
        # ho cercato di evitare da doppia ereditariera'
        while len(self._items) > 0:
            tok = self._items.pop(0)
            assert isinstance(tok, Token), \
                "tok non e' un Token"
                
            tok.delete()
        
        JoinNode.delete(self)
    
    
    
class NccNode(BetaMemory):
    '''
    Parte sinistra del duo Ncc
    '''


    def __init__(self, parent, partner_parent, partner_subnet_count):
        '''
        Constructor
        '''
        self._partner = NccPartnerNode(partner_parent, partner_subnet_count, self)
        
        BetaMemory.__init__(self, parent)
        
        
    def get_partner(self):
        '''
        Restituisce il partner di questo nodo
        @return: NccPartnerNode
        '''
        return self._partner
    
    @staticmethod
    def factory(parent, conds, earlier_conds, builtins, alpha_root):
        
        assert isinstance(parent, ReteNode), \
            "parent non e' un ReteNode"
            
        assert isinstance(earlier_conds, list), \
            "earlier_conds non e' una list"
            
        # costruisce le sotto condizioni della NccCondition
        # come se fossero normali condizioni (e non interne ad una NCC)
        # in modo da poterle condividerle con altre condizioni positive
        # se presenti (o aggiunte in futuro)
        from icse import rete
        last_node = rete.network_factory(alpha_root, parent, conds, earlier_conds, builtins )
        
        assert isinstance(last_node, ReteNode)
                
        for child in parent.get_children():
            # c'e' gia un figlio che e' un NCC
            # e il cui partner mangia dalla stessa sottorete
            # che rappresenta le condizioni di questa NCC
            if isinstance(child, NccNode) \
                    and child.get_partner().get_parent() == last_node:
                # la condivido!
                return child

        # nada, niente da condividere (almeno a livello di NCC)
        
        ncc = NccNode(parent, last_node, len(conds))

        # inserisco i vari riferimenti dei figli nei padri
        parent.append_child(ncc)
        last_node.add_child(ncc.get_partner())

                      
        # completare l'aggiornamento
        # prima devo aggiornare l'NccNode e dopo il partner
        # per evitare che si crei confusione nel buffer nel partner
        
        parent.update(ncc)
        last_node.update(ncc.get_partner())
        
        return ncc
        
    def leftActivation(self, tok, wme):
        
        new_token = Token(self, tok, wme)
        self._items.insert(0, new_token)
        
        results = self.get_partner().flush_resultbuffer()
        for r in results:
            assert isinstance(r, Token), \
                "r non e' un Token"
            new_token.add_nccresult(r)
            
            r.set_owner(new_token)
            
        # controllo se ho trovato match
        if new_token.count_nccresults() == 0:
            # e nel caso non ci siano attivo i figlioli
            
            for child in self.get_children():
                child.leftActivation(new_token)

    def update(self, child):
        '''
        Esegue l'aggiornamento dei figli (attivandoli a sinistra)
        se vengono trovati token che non hanno match per nccresult
        (il nodo e' negativo)
        '''
        for t in self._items:
            assert isinstance(t, Token), \
                "t non e' un Token"
                
            if t.count_nccresults() == 0:
                child.leftActivation(t)

    def delete(self):
        '''
        Esegue la rimozione del nodo dalla rete
        (a seguito della rimozione di una produzione)
        
        L'eliminazione tiene provoca la rimozione
        del partner (e dei padre inutile del partner)
        '''
        self.get_partner().delete()
        
        # chiamo la rimozione di BetaMemory (che se la vedra'
        # per quanto riguarda la rimozione dei token)
        # e poi chiamera' ReteNode.delete() per la pulizia
        # generica
        BetaMemory.delete(self)
        
class NccPartnerNode(ReteNode):
    '''
    Partner node di un NCC sinistro
    (consente di simulare un attivazione
    sinistra da destra)
    '''


    def __init__(self, parent, cond_count, nccnode):
        '''
        Constructor
        '''
        ReteNode.__init__(self, parent)
        
        self._nccnode = nccnode
        self._conjuctions = cond_count
        
        # list of partial-match wating to be read from
        # the ncc-node
        self._resultbuffer = []
        
        
    def flush_resultbuffer(self):
        rb = self._resultbuffer
        self._resultbuffer = []
        return rb
    
    def get_nccnode(self):
        return self._nccnode
    
    def leftActivation(self, tok, wme):
        
        assert isinstance(tok, Token), \
            "tok non e' un Token"
            
        assert isinstance(wme, WME), \
            "wme non e' un WME"
        
        new_result = Token(self, tok, wme)
        
        # Cerchiamo il token padre di questo che possa rappresentare
        # correttamente l'owner del nuovo token.
        # risaliamo il percorso per trovare il token che e' emerso
        # dalla join della precedente condizione
        
        owner_t = tok
        owner_w = wme
        for _ in range(0, self._conjuctions):
            owner_w = owner_t.get_wme()
            owner_t = owner_t.get_parent()
        
        # cerchiamo per un token nella memoria del nodo ncc
        # che abbia gia come owner owner_t trovato e
        # come wme l'wme trovato
        for ncc_token in self._nccnode.get_items():
            assert isinstance(ncc_token, Token)
            if ncc_token.get_parent() == owner_t \
                    and ncc_token.get_wme() == owner_w:
                
                # c'e' ne gia uno
                # aggiungiamo new_result come 
                # nuovo figlio ncc-result del token
                # trovato (e chiaramente colleghiamo come owner
                # l'owner trovato al nuovo result
                ncc_token.add_nccresult(new_result)
                new_result.set_owner(ncc_token)
                
                # visto che il token ha avuto un match
                # dobbiamo provvedere ad eliminare tutti
                # gli eventuali discendenti che ci sono
                # in quanto la condizione negativa
                # non e' piu valida
                
                ncc_token.deleteDescendents()
                
                # abbiamo trovato un match, non ha senso continuare
                # oltre nel ciclo (e nella funzione)
                return
        
        # non abbiamo trovato nessun match nell'ncc-node
        # questo significa che la sotto-rete negativa
        # ha trovato un match ma che il ncc-node
        # non e' ancora stato attivato
        # (in quanto ultimo dei figli del padre della sottorete)
        # memorizzo il risultato nel buffer e aspetto
        # pazientemente l'attivazione
        # del ncc-node
        self._resultbuffer.insert(0, new_result)
        
        
    def delete(self):
        '''
        Pulisce il buffer
        e poi elimino il nodo tramite il 
        delete base
        '''
        while len(self._resultbuffer) > 0:
            # il contenuto del buffer
            # sono token... e per eliminarli
            # chiamo la delete direttamente 
            self._resultbuffer.pop(0).delete()

        # propago la chiamata al metodo
        # base per pulizia di base
        ReteNode.delete(self)

class BetaRootNode(JoinNode):
    '''
    Rappresenta la 
    '''

    def __init__(self, network, alpha_root):
        '''
        Constructor
        '''
        assert isinstance(alpha_root, AlphaRootNode)
        
        self._network = network
        JoinNode.__init__(self, None, alpha_root.get_alphamemory(), [])
        
    def get_network(self):
        return self._network
        
    def get_parent(self):
        return self
        
    def rightActivation(self, wme):
        
        assert isinstance(wme, WME), \
            "wme non e' un WME"
            
        # creo un DummyToken :(
        t = DummyToken(wme, self)
            
        for child in self.get_children():
            assert isinstance(child, ReteNode), \
                "child non e' un ReteNode"
            
            # attiva a sinistra i figli
            # (che sono join-node o simili)
            
            child.leftActivation(t)

    