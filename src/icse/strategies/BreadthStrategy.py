'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import Strategy

class BreadthStrategy(Strategy):
    '''
    Inserisce gli elementi come ultimi in priorita'
    di attivazione per gli elementi con lo stesso salience
    '''

    def insert(self, pnode, token, per_salience_list):
        per_salience_list.append((pnode, token))

    def resort(self, per_saliance_list):
        per_saliance_list.sort(key=lambda x: self._get_max_epoch(x[1]))
    
    def _get_max_epoch(self, token):
        return max([x.get_epoch() for x in token.linearize(False)])
        
