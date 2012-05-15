'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class IntegerDivision(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'div',
                'minParams': 2,
                'handler': Function.handler
            })
        return sign
        
    @staticmethod
    def handler(op1, op2):
        return (int(op1) / int(op2))
    
    