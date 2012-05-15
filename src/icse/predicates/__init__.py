from icse.predicates.Predicate import Predicate


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
    _predicati = {}

    _initied = False

    @staticmethod        
    def call(nome, args = []):
        '''
        Invoca un predicato presente nel dizionario
        di predicati oppure lancia una eccezione se:
            - il tipo o il numero di argomenti
                attesi e' diverso dal richiesto
            - non c'e' una predicato con il nome richiesto
                nel dizionario di funzioni (che viene
                inizializzato all'importazione del package
        '''
        if not Proxy._predicati.has_key(nome):
            raise PredicateNotFoundError("Il predicato richiesto non e' definito: "+str(nome))
        
        func = Proxy._predicati[nome]
        
        return func['handler'](*args)


    @staticmethod
    def get(nome):
        '''
        Restituisce un predicato presente nel dizionario
        di predicati oppure lancia una eccezione se:
            - il tipo o il numero di argomenti
                attesi e' diverso dal richiesto
            - non c'e' una predicato con il nome richiesto
                nel dizionario di funzioni (che viene
                inizializzato all'importazione del package
        '''
        if not Proxy._predicati.has_key(nome):
            raise PredicateNotFoundError("Il predicato richiesto non e' definito: "+str(nome))
        
        func = Proxy._predicati[nome]
        
        return func['cls']
        
    
    @staticmethod
    def define(funcName, handler, cls):
        if Proxy._predicati.has_key(funcName):
            raise DuplicatePredicateError("predicato gia definito: "+funcName)
        
        if not callable(handler):
            raise InvalidHandlerError("L'handler fornito non e' valido")
        
        Proxy._predicati[funcName] = {
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
    def get_predicates():
        return Proxy._predicati
        
             
      
class ProxyError(Exception):
    '''
    Eccezione base lanciata dal Proxy
    '''
    pass
        
class DuplicatePredicateError(ProxyError):
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

class PredicateNotFoundError(ProxyError):
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
                                                                and x != 'Predicate.py' \
                                                                and x != 'Variable.py' \
                                                                and x[0] != '_']
    
    
    for modulo in funzioni:
        if modulo.startswith("."):
            classe = modulo[1:]
            modulo = "icse.predicates"+modulo
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
        
            if issubclass(attr, Predicate):
                sign = attr.sign()
                if isinstance(sign, dict) \
                        and sign.has_key('sign') \
                        and sign['sign'] != None:
                    
                    Proxy.define(sign['sign'], sign['handler'], sign['cls'])
        except Exception, e:
            # ignora l'elemento che inoltra errori
            # raise
            pass
        
    Proxy.set_initied()
