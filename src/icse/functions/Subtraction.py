'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Subtraction(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': '-',
                'minParams': 2,
                'handler': Subtraction.handler
            })
        return sign
        
    @staticmethod
    def handler(op1, op2):
        return (op1 - op2)
    
    