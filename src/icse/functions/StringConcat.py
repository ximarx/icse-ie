'''
Created on 15/mag/2012

@author: Francesco Capozzo
'''
from icse.functions import Function

class StringConcat(Function):
    '''
    classdocs
    '''
    @staticmethod
    def sign():
        sign = Function.sign()
        sign.update({
                'sign': 'str-cat',
                'minParams': 2,
                'handler': StringConcat.handler
            })
        return sign
        
    @staticmethod
    def handler(*args):
        return "".join([str(x) for x in list(args)])
    
    