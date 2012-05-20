'''
Created on 08/mag/2012

@author: Francesco Capozzo
'''
from icse.rete.Token import Token
from icse.rete.Nodes import BetaMemory
from icse.debug import EventManager


class PNode(BetaMemory):
    '''
    Nodo terminale di un ReteNetwork
    Rappresenta una produzioneactivable,
    '''


    def __init__(self, parent,
                 # informazioni sulla produzione
                 name,
                 actions,
                 properties,
                 symbols,
                 # triggers
                 onActive=lambda pnode,token:None,
                 onDeactive=lambda pnode,token:None,
                 assertFunc=lambda fact:(None,None,False),
                 retractFunc=lambda wme:None,
                 addProduction=lambda production:None,
                 removeProduction=lambda pnode:None
                ):
        '''
        Constructor
        '''
        self.__onActive = onActive
        self.__onDeactive = onDeactive
        self.__assertFunc = assertFunc
        self.__retractFunc = retractFunc
        self.__addProduction = addProduction
        self.__removeProduction = removeProduction
        
        self.__actions = actions
        self.__name = name
        self.__symbols = symbols
        self.__properties = properties
        
        # sanitarizza la salience
        try:
            if self.__properties.has_key('salience') \
                and not isinstance(self.__properties['salience'], int):
                self.__properties['salience'] = int(self.__properties['salience'])
        except:
            self.__properties['salience'] = 0

        BetaMemory.__init__(self, parent)
        
    def leftActivation(self, tok, wme=None):
        
        new_token = Token(self, tok, wme)
        self._items.insert(0, new_token)
            
        self.__onActive(self, new_token )
        
    def remove_item(self, tok):
        
        BetaMemory.remove_item(self, tok)
        
        # dopo la rimozione devo anche notificare
        # che l'attivazione non e' piu disponibile
        
        self.__onDeactive(self, tok)
        
    def get_name(self):
        return self.__name
        
    def factory(self, parent):
        raise NotImplementedError
    
    def execute(self, token):
        
        # devo linearizzare il token
        # ed eseguire le azioni
        
        EventManager.trigger(EventManager.E_RULE_FIRED, self, token)
        
        wmes = token.linearize()
        
        variables = self._resolve_variables(wmes)
        
        #from pprint import pprint
        #from icse.actions import Action as ActionProxy
        #pprint(variables)
        
        #pprint(self.__actions)
        
        for (action, args) in self.__actions:
            
            action.execute(args, variables,
                            assertFunc=self.__assertFunc,
                            retractFunc=self.__retractFunc,
                            addProductionFunc=self.__addProduction,
                            removeProductionFunc=self.__removeProduction
                        )
            
        
    def _resolve_variables(self, wmes):
        
        solved_builtins = {}
        
        for (var_name, (cond_index, field_index)) in self.__symbols.items():
            
            wme = wmes[cond_index]
            if wme == None:
                wme = wmes[cond_index + 1]
            
            if field_index == None:
                # il valore e' proprio l'indice della WME
                # NON passo la reference alla wme perche
                # provo a conservare la compatibilita' con CLIPS
                #value = wme.get_factid()
                value = wme
            else:
                # il valore e' il contenuto di un campo
                value = wme.get_field(field_index)
            
            solved_builtins[var_name] = value
        
        return solved_builtins
    
    def get_property(self, propname, default=None):
        try:
            return self.__properties[propname]
        except KeyError:
            return default