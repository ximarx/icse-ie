'''
Created on 30/mar/2012

@author: ximarx
'''
from icse.ps.rules.funzioni.Funzione import Funzione
from icse.ps.Fact import Fact

class Attributo(Funzione):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Funzione.sign()
        sign.update({
                'sign': 'attributo',
                'minParams': 2,
                'handler': Attributo.handler
            })
        return sign
        
    @staticmethod
    def handler(op1, op2):
        '''
        Restituisce il valore di un attributo di un fatto
        @param op1: Fact il fatto di riferimento
        @param op2: string il nome dell'attributo cercato
        @return: mixed
        @raise AssertionError: se il parametro 1 non e' di tipo Fact
        @raise TypeError: se l'attributo non e' nel fatto 
        '''
        
        assert isinstance(op1, Fact), "Atteso tipo Fact come primo parametro, ottenuto: "+str(type(op1))
        op2 = str(op2)
        
        return op1[op2]
    
    