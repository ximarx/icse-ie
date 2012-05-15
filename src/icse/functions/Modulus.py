'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Modulus(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'mod',
                'minParams': 2,
                'handler': Modulus.handler
            })
        return sign
        
    @staticmethod
    def handler(op1, op2):
        return (op1 % op2)
    
    