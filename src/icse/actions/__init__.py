


class Action(object):
        
    @staticmethod
    def actionImpl(*args):
        #esegue realmente l'azione
        pass
        
    @classmethod
    def execute(cls, *args):
        # procedura di binding delle variabili
        # e chiamata all'implementazione
        cls.actionImpl(*args)
        



