'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import Strategy

class MeaStrategy(Strategy):
    '''
    Precedenza delle attivazioni in base
    all'attualita' della prima wme del token utilizzato nell'attivazione
    di regole con lo stesso salience
    '''

    def insert(self, pnode, token, per_salience_list):
        first_epoch = self._get_first_epoch(token.linearize(False))
        
        for index, (_, o_token) in enumerate(per_salience_list):
            if first_epoch >= self._get_first_epoch(o_token.linearize(False)):
                per_salience_list.insert(index, (pnode, token))
                return
                
        per_salience_list.append((pnode, token))
        
    def _get_first_epoch(self, list_of_wme):
        return list_of_wme[0].get_epoch()
    
    def resort(self, per_saliance_list):
        per_saliance_list.sort(key=lambda x: self._get_first_epoch(x[1].linearize(False)), reverse=True)