'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.BetaMemory import BetaMemory
from icse import rete
from icse.rete.ReteNode import ReteNode
from icse.rete.NccPartnerNode import NccPartnerNode
from icse.rete.Token import Token

class NccNode(BetaMemory):
    '''
    Parte sinistra del duo Ncc
    '''


    def __init__(self, parent, partner_parent, partner_subnet_count):
        '''
        Constructor
        '''
        self.__partner = NccPartnerNode(partner_parent, partner_subnet_count, self)
        
        BetaMemory.__init__(self, parent)
        
        
    def get_partner(self):
        '''
        Restituisce il partner di questo nodo
        @return: NccPartnerNode
        '''
        return self.__partner
    
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
        