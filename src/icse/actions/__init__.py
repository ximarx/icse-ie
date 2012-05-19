from icse.predicates.Eq import Eq



class Proxy(object):
    '''
    Esegue una redirect della parte operativa degli 
    operandi "Predicati" verso l'implementazione reale
    '''

    '''
    il formato di predicati una volta riempito:
        'nomepredicato1': {
                'handler': ref a un callable,
                'minParams: numero di parametri minimo
            },
        'nomepredicato2': ...
    '''
    _actions = {}

    _initied = False

    @staticmethod
    def get(nome):
        '''
        Restituisce una azione presente nel dizionario
        di azioni oppure lancia una eccezione se:
            - il tipo o il numero di argomenti
                attesi e' diverso dal richiesto
            - non c'e' una predicato con il nome richiesto
                nel dizionario di funzioni (che viene
                inizializzato all'importazione del package
        '''
        if not Proxy._actions.has_key(nome):
            raise ActionNotFoundError("L'azione richiesta non e' definita: "+str(nome))
        
        func = Proxy._actions[nome]
        
        return func['cls']
        
    
    @staticmethod
    def define(funcName, handler, cls):
        if Proxy._actions.has_key(funcName):
            raise DuplicateActionError("azione gia definita: "+funcName)
        
        Proxy._actions[funcName] = {
                    'handler' : handler,
                    'cls' : cls
                }
        
    @staticmethod
    def initied():
        return Proxy._initied
    
    @staticmethod
    def set_initied():
        Proxy._initied = True
        
    @staticmethod
    def get_actions():
        return Proxy._actions
             
class ProxyError(Exception):
    '''
    Eccezione base lanciata dal Proxy
    '''
    pass
        
class DuplicateActionError(ProxyError):
    '''
    Lanciata durante il tentativo di ridefinire
    una predicato gia definita
    '''
    pass

class InvalidHandlerError(ProxyError):
    '''
    Lanciata quando l'handler fornito non e' valido
    '''
    pass

class ActionNotFoundError(ProxyError):
    '''
    Lanciata se viene richiesta una predicato non
    presente nel dizionario
    '''
    pass
    
class InvalidSignError(ProxyError):
    '''
    Lanciata quando il numero minimo
    di parametri richiesto della predicato
    non e' rispettato
    '''
    pass

             


class Action(object):

    import sys
    _DEVICES = {
                't': sys.stdout,
                'err': sys.stderr
            }
    
    SIGN = None

    def __init__(self, symbols, devices, 
                                    assertFunc=lambda fact:(None,None,False),
                                    retractFunc=lambda wme:None,
                                    addProductionFunc=lambda production:None,
                                    removeProductionFunc=lambda pnode:None
                                ):
        '''
        Constructor
        '''
        self._symbols = symbols
        self._devices = devices
        self._assert = assertFunc
        self._retract = retractFunc
        self._addProduction = addProductionFunc
        self._removeProduction = removeProductionFunc
        
    def assertFact(self, fact):
        self._assert(fact)
        
    def retractFact(self, fact):
        self._retract(fact)
        
    def addProduction(self, production):
        self._addProduction(production)
        
    def removeProduction(self, pnode):
        self._removeProduction(pnode)
        
    def executeImpl(self, *args):
        #esegue realmente l'azione
        pass
        
    @classmethod
    def execute(cls, args, variables,
                                 assertFunc=lambda fact:(None,None,False),
                                 retractFunc=lambda wme:None,
                                 addProductionFunc=lambda production:None,
                                 removeProductionFunc=lambda pnode:None
                            ):
        # sostituisce tutte le variabili
        # all'interno degli argomenti
        # della chiamata ad azione
        
        # instanza una nuovo oggetto del tipo
        # azione desiderata, fornendo al costruttore:
        #     - il dizionario dei simboli risolti (quindi gia avvalorati)
        #            [sara' possibile modificarlo dall'interno della
        #            classe per fare in modo di rendere possibile
        #            il binding di nuove variabili all'interno delle classi]
        #    - il dizionario dei dispositivi disponibili
        instance = cls(variables, Action._DEVICES,
                            assertFunc=assertFunc,
                            retractFunc=retractFunc,
                            addProductionFunc=addProductionFunc,
                            removeProductionFunc=removeProductionFunc
                        )
        return getattr(instance, cls.sign()['handler'])(*args)
        
    @classmethod
    def sign(cls):
        return {
                'sign': cls.SIGN,
                'handler': "executeImpl",
                'cls': cls
            }    

    def _resolve_args(self, unquote=False, recursive=True, *args):
        from icse.Variable import Variable
        from icse.Function import Function
        filtered = []
        for arg in list(args):
            if isinstance(arg, tuple):
                if issubclass(arg[0], Variable):
                    # trasformo la variabile
                    # nel suo valore trovato
                    # attingendo dal dizionario
                    # dei simboli
                    filtered.append(self._symbols[arg[1]])
                elif issubclass(arg[0], Action):
                    # abbiamo una azione in una azione
                    # dobbiamo eseguirla ed inserire il valore
                    # di ritorno come parametro
                    # della funzione
                    actClass = arg[0]
                    returned = actClass.execute(arg[1], self._symbols,
                                assertFunc=self._assert,
                                retractFunc=self._retract,
                                addProductionFunc=self._addProduction,
                                removeProductionFunc=self._removeProduction
                            )
                    filtered.append(returned)
                    
                elif issubclass(arg[0], Function):
                    func_class = arg[0]
                    parametri = arg[1]
                    # risolvo i parametri interni della funzione
                    parametri = self._resolve_args(True, True, *parametri)
                    filtered.append(func_class.get_function().sign()['handler'](*parametri))
                    
                elif issubclass(arg[0], Eq):
                    filtered.append(arg[1])
                    
                # TODO
                # potremmo inserire il processo delle funzioni
                # e dei condizionarli!!!
            elif isinstance(arg, (str, unicode)) and unquote and arg[0] == '"':
                # rimuovo i quote
                filtered.append(arg[1:-1])
            elif isinstance(arg, list) and recursive:
                # ripeto l'operazione per tutti gli elementi del vettore
                filtered.append(self._resolve_args(unquote, recursive, *arg))
            else:
                # se e' un normale valore semplicemente
                # lo aggiungo
                filtered.append(arg)  
        
        return filtered

if not Proxy.initied():
#if False:
    
#    funzioni = [
#        '.Somma',
#        '.Prodotto',
#        '.Sottrazione',
#        '.Divisione',
#        '.Potenza',
#        '.Radice',
#        '.Attributo'
#    ]

    import os
    from genericpath import isfile
    
    FUNCS_DIR = os.path.dirname(__file__)
    
    funzioni = ['.'+x[0:-3] for x in os.listdir(FUNCS_DIR) if isfile(FUNCS_DIR + "/" +x) \
                                                                and x[-3:] == '.py' \
                                                                and x[0] != '_']
    
    
    for modulo in funzioni:
        if modulo.startswith("."):
            classe = modulo[1:]
            modulo = "icse.actions"+modulo
        else:
            lastdot = modulo.rfind('.')
            classe = modulo[lastdot+1:]
            modulo = modulo[0:lastdot]
        
        #print "Modulo: ",modulo
        #print "Classe: ",classe
            
        try:
            imported = __import__(modulo,  globals(), locals(), [classe], -1)
            attr = getattr(imported, classe)
        
            #print "Canonical: ",attr
        
            if issubclass(attr, Action):
                sign = attr.sign()
                if isinstance(sign, dict) \
                        and sign.has_key('sign') \
                        and sign['sign'] != None:
                    
                    Proxy.define(sign['sign'], sign['handler'], sign['cls'])
        except Exception, e:
            # ignora l'elemento che inoltra errori
            #raise
            pass
        
    Proxy.set_initied()
