


class Action(object):

    import sys
    _DEVICES = {
                't': sys.stdout,
                'err': sys.stderr
            }

    def __init__(self, symbols, devices):
        '''
        Constructor
        '''
        self._symbols = symbols
        self._devices = devices

    @staticmethod
    def get_ebnf():
        pass
    
    @staticmethod
    def parse_action():
        pass
        
    def executeImpl(self, *args):
        #esegue realmente l'azione
        pass
        
    @classmethod
    def execute(cls, args, variables):
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
        instance = cls(variables, Action._DEVICES)
        return instance.executeImpl(*args)
        
        



