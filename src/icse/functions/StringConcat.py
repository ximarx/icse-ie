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
#        return '"'+"".join([str(x) if isinstance(x, (str,unicode)) and x[0] != '"'
#                        else str(x)[1,-1] if isinstance(x, (str,unicode)) and x[0] == '"'
#                        else str(x)
#                        for x in list(args)])+'"'
        to_string = [str(x) for x in list(args)]
        unquoted = [x if x[0] != '"' else x[1:-1] for x in to_string]
        return '"'+ "".join(unquoted) + '"'
            
    