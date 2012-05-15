'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class StringLength(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'str-length',
                'minParams': 1,
                'handler': StringLength.handler
            })
        return sign
        
    @staticmethod
    def handler(op):
        return len(op)
    
    