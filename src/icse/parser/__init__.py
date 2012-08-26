
from icse.parser.ClipsEbnf import ClipsEbnf



def parse(text, debug=False, strict=False):
    '''
    Legge una stringa
    '''
    
    if not strict:
        parser = ClipsEbnf.get_parser(debug)
    
    return parser.parseString(text, True)[:]
    
    
def parseFile(filepath, debug=False):
    
    filer = open(filepath, 'r')
    return parse(filer.read(), debug)
    
    
    
def debug_parsed(items):
    
    for (_, item) in items:
        if isinstance(item, dict):
            for (k,v) in item.items():
                if isinstance(v, dict):
                    print "{0} : {{\n{1}\n}}".format(k,
                                        "\n".join(
                                            ["\t{0} : {1}".format(kk, vv) for (kk,vv) in v.items()]
                                        )
                                    )
                elif isinstance(v, list):
                    print "{0} : [\n\t{1}\n]".format(k,
                                        "\n\t".join([repr(x) for x in v])
                                    )
                else:
                    print "{0} : {1}".format(k, v)
        elif isinstance(item, list):
            for x in item:
                print x
        else:
            print item
    
    
    
    
def new_parser_bridge(text, debug=False):
    
    from myclips.parser.Parser import Parser
    
    parser = Parser(debug, None, True, True)

    parsed = parser.getSParser("CLIPSProgramParser").parseString(text)
    
    print parsed
    
#override normal parse function
#parse = new_parser_bridge
