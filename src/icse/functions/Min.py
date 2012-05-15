'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Min(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'min',
                'minParams': 2,
                'handler': Min.handler
            })
        return sign
        
    @staticmethod
    def handler(*args):
        return min(list(args))
    
    