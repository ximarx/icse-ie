'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Integer(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'integer',
                'minParams': 1,
                'handler': Integer.handler
            })
        return sign
        
    @staticmethod
    def handler(op):
        return float(op)
    
    