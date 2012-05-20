from icse.rete.ReteNetwork import ReteNetwork
from icse.Production import Production
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper

import icse.parser as clipsparser
from genericpath import isfile, exists
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
    
    #agenda = rete.agenda()
    #from icse.rete.Agenda import Agenda
    #assert isinstance(agenda, Agenda)
    
    parseQueue = []
    parsedModuleCache = {}
    
    stats_defrule = 0
    stats_deffacts = 0
    stats_facts = 0
    stats_modules = 0
    
    current_file = filepath
    
    while len(parsedItems) > 0 or len(parseQueue) > 0:
    
        for (item_type, item) in parsedItems:
            if item_type == 'defrule':
                rule = item
                default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
                default_rule.update(rule)
                rule = default_rule
                p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
                rete.add_production(p)
                stats_defrule += 1
            elif item_type == 'deffacts':
                stats_deffacts += 1
                for fact in item:
                    stats_facts += 1
                    rete.assert_fact(fact)
            elif item_type == 'set-strategy':
                rete.agenda().changeStrategy(item)
            elif item_type == 'myclips-directive':
                # processo le direttive
                dir_type, dir_arg = item
                if dir_type == 'include':
                    # inclusione di file al termine della lettura di questo
                    import os
                    module_path = os.path.dirname(current_file) + '/' + dir_arg
                    if isfile( module_path ):
                        parseQueue.append(module_path)
                        #print "Modulo preparato alla lettura: ", os.path.dirname(filepath) + '/' + dir_arg
                    else:
                        print "File non valido: ", module_path
            
        parsedItems = []
                
        if len(parseQueue) > 0:
            pmodule = parseQueue.pop(0)
            if not parsedModuleCache.has_key(pmodule):
                parsedModuleCache[pmodule] = True
                stats_modules += 1
                try:
                    current_file = pmodule
                    parsedItems = clipsparser.parseFile(pmodule, DEBUG)
                except:
                    print "Errore durante il caricamento del modulo: ", pmodule
                    parsedModuleCache[pmodule] = False
    

    print
    print "-------------------"
    print "Statistiche:"
    print "    defrule:            ", stats_defrule
    print "    deffacts:           ", stats_deffacts
    print "    facts:              ", stats_facts
    print "    myclips-modules:    ", stats_modules
    
    
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

    #NetworkXGraphWrapper.i().draw()
        
    print "-------------------"
    print "Esecuzione: "
    print
    
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
#
#        raw_input() # attende invio
#        
        
        node, token = agenda.get_activation()
        print "\t\t\t\t\t\t[{0}]".format(node.get_name())
        node.execute(token)
        # non e' necessario aggiornare
        # l'agenda visto che e' un riferimento
        # agli attivabili
        #agenda = rete.agenda()

        
    print
    print "--------------------"
    print "Post esecuzione:"
    print
    
    for wme in sorted(rete.get_wmes(), key=lambda x: x.get_factid()):
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
    tests = sorted([x for x in os.listdir(TESTS_DIR) if isfile(TESTS_DIR + "/" +x) and x[-4:] == '.clp'])
    
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
                
    