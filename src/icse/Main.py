from icse.rete.ReteNetwork import ReteNetwork
from icse.Production import Production
from icse.rete.NetworkXGraphWrapper import NetworkXGraphWrapper
from icse.debug import EventManager, ConsoleDebugMonitor, ReteRenderer
import icse.parser as clipsparser

from genericpath import isfile
import traceback
import sys
from pyparsing import ParseException


def execute_test(filepath):
    
    EventManager.reset()
    
    DEBUG = False
    parseError = False
    try:
        parsedItems = clipsparser.parseFile(filepath, DEBUG)
    except ParseException, e:
        
        parseError = True
        
        print "Errore nel file: ", filepath
        print "    [dopo] Riga:         ", e.lineno
        print "    [dopo] Colonna:      ", e.col
        print "    [dopo] Testo:        ", e.line
        print "    Messaggio:           ", str(e)
        print
    
    except Exception, e2:
        parseError = True
        
        print e2
        
    finally:

        # in caso di eccezione del parser, e debug falso
        # eseguo nuovamente
        if parseError: 
            if not DEBUG:
                print "Vuoi attivare la modalita' debug del parser? (si/no)"
                risposta = raw_input()
                if risposta.lower() == "si":
                    parsedItems = clipsparser.parseFile(filepath, True)
                else:
                    return
            else:
                return            
        
    if DEBUG:
        clipsparser.debug_parsed(parsedItems)

    rete = ReteNetwork()
    
    DM = ConsoleDebugMonitor()
    DM.linkToEventManager(EventManager)
    
    RR = ReteRenderer()
    RR.linkToEventManager(EventManager)
    
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
                    module_path = os.path.realpath( os.path.dirname(current_file) + '/' + dir_arg )
                    if isfile( module_path ):
                        parseQueue.append(module_path)
                        #print "Modulo preparato alla lettura: ", os.path.dirname(filepath) + '/' + dir_arg
                    else:
                        print "File non valido: ", module_path
                elif dir_type == 'debug':
                    #argomenti di debug nella forma:
                    #    chiave=valore,chiave2=valore2,ecc
                    try:
                        debug_infos = dict([tuple(x.strip().split('=')) for x in dir_arg.strip().split(',')])
                        EventManager.trigger( EventManager.E_DEBUG_OPTIONS_CHANGED, debug_infos, rete)
                    except Exception, e:
                        #ignora la direttiva se il formato non e' corretto
                        print e
                        print >> sys.stderr, "Direttiva debug ignorata: ", dir_arg  
                    
                    
                    
            
        parsedItems = []
                
        if len(parseQueue) > 0:
            pmodule = parseQueue.pop(0)
            if not parsedModuleCache.has_key(pmodule):
                parsedModuleCache[pmodule] = True
                stats_modules += 1
                try:
                    print "Caricamento modulo: ", pmodule
                    current_file = pmodule
                    parsedItems = clipsparser.parseFile(pmodule, DEBUG)
                    EventManager.trigger( EventManager.E_MODULE_INCLUDED, pmodule)
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
    
    EventManager.trigger(EventManager.E_NETWORK_READY, rete)
        
    print "-------------------"
    print "Esecuzione: "
    print
    
    while not agenda.isEmpty():
        # il get_activation rimuove la regola dall'agenda automaticamente
        node, token = agenda.get_activation()
        node.execute(token)

        
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
                
    