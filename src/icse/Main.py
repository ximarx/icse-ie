from icse.rete.ReteNetwork import ReteNetwork
from icse.Production import Production
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper

import icse.parser as clipsparser
from genericpath import isfile
import traceback
import sys


def execute_test(filepath):
    
    DEBUG = False
    try:
        parsedItems = clipsparser.parseFile(filepath, DEBUG)
    except Exception:
        # in caso di eccezione del parser, e debug falso
        # eseguo nuovamente
        if not DEBUG:
            parsedItems = clipsparser.parseFile(filepath, True)            
        else:
            raise    
        
    if DEBUG:
        clipsparser.debug_parsed(parsedItems)
            
    
    NetworkXGraphWrapper.i().set_debug(DEBUG)
    
    rete = ReteNetwork()
    facts_count = 0
    
    for (item_type, item) in parsedItems:
        if item_type == 'defrule':
            rule = item
            default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
            default_rule.update(rule)
            rule = default_rule
            p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
            rete.add_production(p)
        elif item_type == 'deffacts':
            for fact in item:
                facts_count += 1
                rete.assert_fact(fact)

    print
    print "-------------------"
    print "Statistiche:"
    print "    defrule:     ", len([x for (x,_) in parsedItems if x == 'defrule' ])
    print "    deffacts:    ", len([x for (x,_) in parsedItems if x == 'deffacts' ])
    print "    facts:       ", facts_count
    
    
    print
    print "-------------------"
    print "Agenda: "
    agenda = rete.agenda()
    for (salience, pnode, token) in agenda.activations():
        print "{0} {1}:\t{2}".format(
                           str(salience).ljust(6, ' '),
                           pnode.get_name(),
                           ", ".join(['f-'+str(w.get_factid()) for w in token.linearize(False)])
                        ) 

        
    print "-------------------"
    print "Esecuzione: "
    print
    
    #NetworkXGraphWrapper.i().draw()
    
    while not agenda.isEmpty():
#        print "\t\t\t---Stato WM---"
#        for wme in rete.get_wmes():
#            print "\t\t\t{0} ({1})".format(
#                                    str("f-"+str(wme.get_factid())).ljust(5, ' '),
#                                    " ".join([str(x) for x in wme.get_fact()]) if isinstance(wme.get_fact(), list) 
#                                        else str(wme.get_facts()) 
#                                )
#        print "\t\t\t---Agenda:---"
#        agenda = rete.agenda()
#        for (salience, pnode, token) in agenda.activations():
#            print "\t\t\t{0} {1}:\t{2}".format(
#                               str(salience).ljust(6, ' '),
#                               pnode.get_name(),
#                               ", ".join(['f-'+str(w.get_factid()) for w in token.linearize(False)])
#                            ) 

        node, token = agenda.get_activation()
        node.execute(token)
        # non e' necessario aggiornare
        # l'agenda visto che e' un riferimento
        # agli attivabili
        #agenda = rete.agenda()

        
    print
    print "--------------------"
    print "Post esecuzione:"
    print
    
    for wme in rete.get_wmes():
        print "{0} ({1})".format(
                                str("f-"+str(wme.get_factid())).ljust(5, ' '),
                                " ".join([str(x) for x in wme.get_fact()]) if isinstance(wme.get_fact(), list) 
                                    else str(wme.get_facts()) 
                            )
    
    
    #NetworkXGraphWrapper.i().draw()
    NetworkXGraphWrapper.i().clear()
                
def main_loop():                
                
    import os            
    
    TESTS_DIR = os.getcwd()+'/../../tests'
    
    print "TESTS_DIR: ", TESTS_DIR
    print 
    
    #print os.listdir(TESTS_DIR)
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
                
    