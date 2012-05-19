'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import Strategy

class LexStrategy(Strategy):
    '''
    Precedenza delle attivazioni in base
    all'attualita' dei token utilizzati nell'attivazione
    di regole con lo stesso salience
    '''

    def insert(self, pnode, token, per_salience_list):
        sorted_epoch = self._sort_epoch(token.linearize(False))
        
        for index, (_, o_token) in enumerate(per_salience_list):
            if sorted_epoch >= self._sort_epoch(o_token.linearize(False)):
                per_salience_list.insert(index, (pnode, token))
                return
                
        per_salience_list.append((pnode, token))
        
    def _sort_epoch(self, list_of_wme):
        return sorted(list_of_wme, key=lambda x:x.get_epoch())
    
    def resort(self, per_saliance_list):
        per_saliance_list.sort(key=lambda x: self._sort_epoch(x[1]) )
        
    