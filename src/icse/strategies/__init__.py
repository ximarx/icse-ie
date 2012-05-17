

class Strategy(object):
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
    def insert(self, pnode, token, per_salience_list):
        raise NotImplementedError
    
    def resort(self, per_saliance_list):
        raise NotImplementedError
    
    
class DepthStrategy(Strategy):
    '''
    Inserisce le nuove attivazioni
    in testa alla coda delle attivazioni
    per la stessa salience
    '''
    
    def insert(self, pnode, token, per_salience_list):
        per_salience_list.insert(0, (pnode, token))
    
    def resort(self, per_saliance_list):
        per_saliance_list.sort(key=lambda x: self._get_max_epoch(x[1]), reverse=True)
    
    def _get_max_epoch(self, token):
        return max([x.get_epoch() for x in token.linearize(False)])
        
    
class StrategyManager(object):
    
    _DEFAULT_STRATEGY = None
    _DEFAULT_STRATEGY_CLASS = DepthStrategy
    
    @staticmethod
    def strategy():
        if StrategyManager._DEFAULT_STRATEGY == None:
            StrategyManager._DEFAULT_STRATEGY = StrategyManager._DEFAULT_STRATEGY_CLASS()
           
        return StrategyManager._DEFAULT_STRATEGY
    
    @staticmethod
    def set_default_strategy(strategy):
        assert isinstance(strategy, Strategy)
        StrategyManager._DEFAULT_STRATEGY = strategy
    
    @staticmethod
    def reset_strategy():
        StrategyManager._DEFAULT_STRATEGY = None
        