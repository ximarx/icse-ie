'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import Strategy
import random

class RandomStrategy(Strategy):
    '''
    Inserisce gli elementi in ordine casuale
    di attivazione per gli elementi con lo stesso salience
    '''

    def insert(self, pnode, token, per_salience_list):
        rand_index = random.randrange(0, len(per_salience_list))
        per_salience_list.insert(rand_index, (pnode, token))

    def resort(self, per_saliance_list):
        random.shuffle(per_saliance_list)

        
        
