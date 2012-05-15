'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Float(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'float',
                'minParams': 1,
                'handler': Float.handler
            })
        return sign
        
    @staticmethod
    def handler(op):
        return float(op)
    
    