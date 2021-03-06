'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Multiplication(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': '*',
                'minParams': 2,
                'handler': Multiplication.handler
            })
        return sign
        
    @staticmethod
    def handler(op1, op2):
        return (op1 * op2)
    
    