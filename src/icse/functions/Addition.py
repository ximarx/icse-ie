'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class Addition(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': '+',
                'minParams': 2,
                'handler': Addition.handler
            })
        return sign
        
    @staticmethod
    def handler(*args):
        return sum(args)
    
    