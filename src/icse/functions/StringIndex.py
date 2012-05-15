'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class StringIndex(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'str-index',
                'minParams': 2,
                'handler': StringIndex.handler
            })
        return sign
        
    @staticmethod
    def handler(needle, haystack):
        # in clips:
        #    l'array e' 1-index
        #    ritorna False se non c'e' la stringa
        pos = str(haystack).find(str(needle))
        return (pos + 1) if pos != -1 else False  
    
    