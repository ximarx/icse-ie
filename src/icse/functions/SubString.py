'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class SubString(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'sub-string',
                'minParams': 3,
                'handler': SubString.handler
            })
        return sign
        
    @staticmethod
    def handler(start, end, op):
        if start < 1: start = 1
        if end < start: return ""
        return str(op)[start-1, end]
    
    