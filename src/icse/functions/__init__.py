

class Proxy(object):
    '''
    Esegue una redirect della parte operativa degli 
    operandi "Funzione" verso l'implementazione reale
    '''

    '''
    il formato di funzioni una volta riempito:
        'nomefunzione1': {
                'handler': ref a un callable,
                'minParams: numero di parametri minimo
            },
        'nomefunzione2': ...
    '''
    _funzioni = {}

    _initied = False

    @staticmethod        
    def call(nome, args = []):
        '''
        Invoca una funzione presente nel dizionario
        di funzioni oppure lancia una eccezione se:
            - il tipo o il numero di argomenti
                attesi e' diverso dal richiesto
            - non c'e' una funzione con il nome richiesto
                nel dizionario di funzioni (che viene
                inizializzato all'importazione del package
        '''
        if not Proxy._funzioni.has_key(nome):
            raise FunctionNotFoundError("La funzione richiesta non e' definita: "+str(nome))
        
        func = Proxy._funzioni[nome]
        if func['minParams'] > len(args):
            raise InvalidSignError("Il numero minimo di parametri ("+func['minParams']+") per la funzione "+nome+" non e' stato rispettato: "+len(args)+" forniti")
        
        return func['handler'](*args)

        
    @staticmethod
    def get(nome):
        if not Proxy._funzioni.has_key(nome):
            raise FunctionNotFoundError("La funzione richiesta non e' definita: "+str(nome))
        
        func = Proxy._funzioni[nome]
        return func['cls']
    
    @staticmethod
    def define(funcName, handler, cls, minParams = 0):
        if Proxy._funzioni.has_key(funcName):
            raise DuplicateFunctionError("Funzione gia definita: "+funcName)
        
        if not callable(handler):
            raise InvalidHandlerError("L'handler fornito non e' valido")
        
        Proxy._funzioni[funcName] = {
                    'handler' : handler,
                    'minParams' : minParams,
                    'cls': cls
                }
        
    @staticmethod
    def initied():
        return Proxy._initied
    
    @staticmethod
    def set_initied():
        Proxy._initied = True
        
    @staticmethod
    def get_functions():
        return Proxy._funzioni
        
        
class Function(object):
    '''
    Realizzazione concreta di funzione
    '''

    @staticmethod
    def handler():
        '''
        '''

    @staticmethod
    def sign():
        return {
                'sign': 'deffunc',
                'minParams': 2,
                'handler': Function.handler
            }
             
      
class ProxyError(Exception):
    '''
    Eccezione base lanciata dal Proxy
    '''
    pass
        
class DuplicateFunctionError(ProxyError):
    '''
    Lanciata durante il tentativo di ridefinire
    una funzione gia definita
    '''
    pass

class InvalidHandlerError(ProxyError):
    '''
    Lanciata quando l'handler fornito non e' valido
    '''
    pass

class FunctionNotFoundError(ProxyError):
    '''
    Lanciata se viene richiesta una funzione non
    presente nel dizionario
    '''
    pass
    
class InvalidSignError(ProxyError):
    '''
    Lanciata quando il numero minimo
    di parametri richiesto della funzione
    non e' rispettato
    '''
    pass



if not Proxy.initied():
    
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
    
    funzioni = ['.'+x[0:-3] for x in os.listdir(FUNCS_DIR) if isfile(FUNCS_DIR + "/" +x) and x[-3:] == '.py' and x[0] != '_']
    
    
    for modulo in funzioni:
        if modulo.startswith("."):
            classe = modulo[1:]
            modulo = "icse.functions"+modulo
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
        
            if issubclass(attr, Function):
                sign = attr.sign()
                Proxy.define(sign['sign'], sign['handler'], attr, sign['minParams'])
        except Exception, e:
            # ignoro gli elementi che creano errori
            #raise
            pass
        
    Proxy.set_initied()

