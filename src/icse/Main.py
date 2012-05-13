from icse.rete.ReteNetwork import ReteNetwork
from icse.Production import Production
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper

import icse.parser as clipsparser
from genericpath import isfile
import traceback
import sys


def execute_test(filepath):
    
    DEBUG = False
    
    parsedItems = clipsparser.parseFile(filepath, DEBUG)
    if DEBUG:
        clipsparser.debug_parsed(parsedItems)
    
    rete = ReteNetwork()
    
    for (item_type, item) in parsedItems:
        if item_type == 'defrule':
            rule = item
            default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
            default_rule.update(rule)
            rule = default_rule
            p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare']['salience'], rule['description'])
            rete.add_production(p)
        elif item_type == 'deffacts':
            for fact in item:
                rete.assert_fact(fact)
    
    agenda = rete.agenda()
    
    print
    print "-------------------"
    print "Agenda: "
    for (node, token) in agenda:
        print "{0}: {1}".format(node.get_name(), token.linearize())
    
    
    
    NetworkXGraphWrapper.i().draw()    
                
                
def main_loop():                
                
    import os            
    
    TESTS_DIR = os.getcwd()+'/../../tests'
    
    print "TESTS_DIR: ", TESTS_DIR
    print 
    
    print os.listdir(TESTS_DIR)
    tests = [x for x in os.listdir(TESTS_DIR) if isfile(TESTS_DIR + "/" +x) and x[-4:] == '.clp']
    
    if len(tests) < 1:
        print "Non ho trovato nessun file di test. Ciao ciao...."
        return False

    while True:
    #if True:
    
        print "Questi sono i file che ho trovato:"
        for i, test in enumerate(tests):
            print "\t"+str(i)+") "+str(test)
            
        print "\t.) Qualsiasi altra selezione per uscire"
        
        try:
            choosed = int(raw_input('Cosa vuoi eseguire? '))
            #choosed = 1
            print "Hai scelto: "+str(tests[choosed])
            print
            print "--------------------------------"
            try:
                execute_test(TESTS_DIR+"/"+tests[choosed])
            except Exception:
                traceback.print_exc(file=sys.stdout)
            print "--------------------------------"
            print
            
        except ValueError:
            print "...Ciao Ciao..."
            return True
    
                
                
if __name__ == '__main__':
    
    main_loop()
                
    