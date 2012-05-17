'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from icse.strategies import Strategy

class SemplicityStrategy(Strategy):
    '''
    Inserisce gli elementi con la stessa salience
    ordinandoli in base al loro indice di complessita'
    Priorita' maggiore agli elementi con indice inferiore
    '''

    def insert(self, pnode, token, per_salience_list):
        
        rule_specificity = pnode.get_property('specificity', 0)
        
        for index, (o_pnode, _) in enumerate(per_salience_list):
            if o_pnode.get_property('specificity', 0) >= rule_specificity:
                # lo inserisce prima del primo elemento
                # con indice di complessita' uguale
                # o maggiore
                per_salience_list.insert(index, (pnode, token))
                return
            
        per_salience_list.append((pnode, token))

    def resort(self, per_saliance_list):
        per_saliance_list.sort(key=lambda x: x[1].get_property('specificity', 0))
    
        
