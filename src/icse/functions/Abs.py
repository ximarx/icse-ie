'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Abs(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'abs',
                'minParams': 1,
                'handler': Abs.handler
            })
        return sign
        
    @staticmethod
    def handler(op):
        return abs(op)
    
    