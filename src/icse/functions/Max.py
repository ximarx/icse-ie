'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Max(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'max',
                'minParams': 2,
                'handler': Max.handler
            })
        return sign
        
    @staticmethod
    def handler(*args):
        return max(list(args))
    
    