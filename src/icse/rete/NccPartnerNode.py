'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.ReteNode import ReteNode
from icse.rete.Token import Token
from icse.rete.WME import WME

# per adesso lo faccio estendere un ReteNode,
# ma valutare la possibilita' di far estendere
# un JoinNode
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
        
        self.__nccnode = nccnode
        self.__conjuctions = cond_count
        
        # list of partial-match wating to be read from
        # the ncc-node
        self.__resultbuffer = []
        
        
    def flush_resultbuffer(self):
        rb = self.__resultbuffer
        self.__resultbuffer = []
        return rb
    
    def get_nccnode(self):
        return self.__nccnode
    
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
        for i in range(0, self.__conjuctions):
            owner_w = owner_t.get_wme()
            owner_t = owner_t.get_parent()
        
        # cerchiamo per un token nella memoria del nodo ncc
        # che abbia gia come owner owner_t trovato e
        # come wme l'wme trovato
        for ncc_token in self.__nccnode.get_items():
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
        self.__resultbuffer.insert(0, new_result)
        
        
    def delete(self):
        '''
        Pulisce il buffer
        e poi elimino il nodo tramite il 
        delete base
        '''
        while len(self.__resultbuffer) > 0:
            # il contenuto del buffer
            # sono token... e per eliminarli
            # chiamo la delete direttamente 
            self.__resultbuffer.pop(0).delete()

        # propago la chiamata al metodo
        # base per pulizia di base
        ReteNode.delete(self)
