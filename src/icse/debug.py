'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''

from icse.NetworkXGraphWrapper import NetworkXGraphWrapper

def show_wme_details(wme, indent=4, explodeToken=False, maxDepth=3, explodeAMem=False):

    from icse.rete.WME import WME
    
    assert isinstance(wme, WME)

    IP = "".rjust(indent, ' ')

    tokens = wme._WME__tokens

    print IP, "WME: f-", wme.get_factid()," ", wme.get_fact()
    print IP, "  |- TOKENS: ", len(tokens)
    for token in tokens:
        if not explodeToken:
            print IP, "  :  |- ",repr(token)
        else:
            show_token_details(token, indent+8, False, maxDepth-1)
    print IP, "  |- Alpha-Memories: ", len(wme._WME__alphamemories)
    for am in wme._WME__alphamemories:
        if not explodeAMem:
            print IP, "  :  |- " ,repr(am)
        else:
            show_alphamemory_details(am, indent+8, False, maxDepth-1)
            
def show_alphamemory_details(am, indent=4, explodeWme=False, maxDepth=2):

    from icse.rete.Nodes import AlphaMemory, AlphaRootNode

    
    IP = "".rjust(indent, ' ')
    if maxDepth <= 0:
        print IP, '*** MAX-DEPTH ***'
        return

    assert isinstance(am, AlphaMemory)
    
    print IP, "AlphaMemory: ",repr(am)
    print IP, "  |- PARENT: "
    parent = am.get_parent()
    pindent = IP
    while parent != None and not isinstance(parent, AlphaRootNode):
        pindent = pindent + "        "
        print pindent, "  |- Node: ", parent
        print pindent, "  :    |- PARENT:"
        pindent += "    "
        parent = parent.get_parent()
    
    print IP, "  |- WMES: ", len(am.get_items())
    for wme in am.get_items():
        if not explodeWme:
            print IP, "  :  |- ", wme
        else:
            show_wme_details(wme, indent+8, False, maxDepth-1, False)
        
    
def show_token_details(token, indent=4, explodeWme=False, maxDepth=2):

    from icse.rete.Token import Token

    
    IP = "".rjust(indent, ' ')
    
    if maxDepth <= 0:
        print IP, '*** MAX-DEPTH ***'
        return
    
    assert isinstance(token, Token)
    
    
    
    print IP, "Token: ",repr(token)
    print IP, "  |- wme: ", token.get_wme()
    print IP, "  |- node: ", token.get_node()
    print IP, "  |- PARENT: "
    ttok = token.get_parent()
    tindent = IP + "        " 
    while ttok != None:
        print tindent, "  |- Token: ", repr(ttok)
        print tindent, "  :    |- wme: ", ttok.get_wme()
        print tindent, "  :    |- #children: ", len(ttok._Token__children)
        print tindent, "  :    |- node: ", ttok.get_node()
        print tindent, "  :    |- PARENT:"
        tindent = tindent + "            "
        ttok = ttok.get_parent()
    print IP, "  |- CHILDREN: ", len(token._Token__children)
    for subtoken in token._Token__children:
        show_token_details(subtoken, indent+8, False, maxDepth-1 )
    print IP, "  |- NEGATIVE-JOIN-RESULTS: ", len(token._Token__njresults)
    for res in token._Token__njresults:
        print IP, "  :  |- ", res
        print IP, "     :  |- wme: ", res.get_wme()
        print IP, "     :  |- token: ", res.get_owner()
    
def draw_network_fragment(self, lastnode):
    self._gWrapper = NetworkXGraphWrapper.i()

    
class ConsoleDebugMonitor(object):
    
    def __init__(self):
        self._em = None
    
    def linkToEventManager(self, em):
        if self._em != None:
            em.unregister(EventManager.E_DEBUG_OPTIONS_CHANGED, self.onDebugOptionsChange)
            
        if issubclass(em, EventManager):
            self._em = em
            self._em.register(EventManager.E_DEBUG_OPTIONS_CHANGED, self.onDebugOptionsChange)
            
        
    def onDebugOptionsChange(self, changedOptions, *args):
        if isinstance(changedOptions, dict):
            for (key, value) in changedOptions.items():
                method = "_option_"+key
                if hasattr(self, method) \
                        and callable(getattr(self, method)):
                    print key, ' = ', value
                    getattr(self, method)(value)
    
    def _option_watch_rule_fire(self, value):
        if bool(value):
            self._em.register(EventManager.E_RULE_FIRED, self.onRuleFired)
        else:
            self._em.unregister(EventManager.E_RULE_FIRED, self.onRuleFired)

    def _option_watch_rule_activation(self, value):
        if bool(value):
            self._em.register(EventManager.E_RULE_ACTIVATED, self.onRuleActivated)
        else:
            self._em.unregister(EventManager.E_RULE_ACTIVATED, self.onRuleActivated)

    def _option_watch_rule_deactivation(self, value):
        if bool(value):
            self._em.register(EventManager.E_RULE_DEACTIVATED, self.onRuleDeactivated)
        else:
            self._em.unregister(EventManager.E_RULE_DEACTIVATED, self.onRuleDeactivated)
            
    def _option_watch_fact_assert(self, value):
        if bool(value):
            self._em.register(EventManager.E_FACT_ASSERTED, self.onFactAsserted)
        else:
            self._em.unregister(EventManager.E_FACT_ASSERTED, self.onFactAsserted)

    def _option_watch_fact_retract(self, value):
        if bool(value):
            self._em.register(EventManager.E_FACT_RETRACTD, self.onFactRetracted)
        else:
            self._em.unregister(EventManager.E_FACT_RETRACTD, self.onFactRetracted)
            
    def _option_watch_strategy_change(self, value):
        if bool(value):
            self._em.register(EventManager.E_STRATEGY_CHANGED, self.onStrategyChanged)
        else:
            self._em.unregister(EventManager.E_STRATEGY_CHANGED, self.onStrategyChanged)
    
            
    def onRuleFired(self, pnode, token, *args):
        print "\n\t\t\t\t\t[{0}: {1}]".format(pnode.get_name(), ", ".join(['f-'+str(w.get_factid()) for w in token.linearize(False)]))

    def onRuleActivated(self, pnode, token, *args):
        print "\t\t\t\t\t\t+ [{0}: {1}]".format(pnode.get_name(), ", ".join(['f-'+str(w.get_factid()) for w in token.linearize(False)]))
        
    def onRuleDeactivated(self, pnode, token, *args):
        print "\t\t\t\t\t\t- [{0}: {1}]".format(pnode.get_name(), ", ".join(['f-'+str(w.get_factid()) for w in token.linearize(False)]))
    
    def onFactAsserted(self, wme, isNew, *args):
        print "\t\t\t\t\t\t{0} f-{1}: {2}".format(
                                                "+" if isNew else "=",
                                                wme.get_factid(),
                                                wme.get_fact()
                                            )
    def onFactRetracted(self, wme, *args):
        print "\t\t\t\t\t\t- f-{0}: {1}".format(
                                                wme.get_factid(),
                                                wme.get_fact()
                                            )
        
    def onStrategyChanged(self, strategy, *args):
        print "\t\t\t\t\t\t# Strategia: {0}".format(
                                                strategy.__class__.__name__
                                            )
        

class ReteRenderer(object):
    
    def __init__(self):
        self._em = None
        self._gWrapper = None
        self._prevStatus = False
    
    def linkToEventManager(self, em):
        if self._em != None:
            em.unregister(EventManager.E_DEBUG_OPTIONS_CHANGED, self.onDebugOptionsChange)
            
        if issubclass(em, EventManager):
            self._em = em
            self._em.register(EventManager.E_DEBUG_OPTIONS_CHANGED, self.onDebugOptionsChange)
         
        self._gWrapper = None   
        #self._gWrapper = NetworkXGraphWrapper.i()
        
    def onDebugOptionsChange(self, changedOptions, rete, *args):
        if isinstance(changedOptions, dict):
            for (key, value) in changedOptions.items():
                method = "_option_"+key
                if hasattr(self, method) \
                        and callable(getattr(self, method)):
                    print key, ' = ', value
                    getattr(self, method)(value, rete)

    def _option_draw_graph(self, value, rete):
        if self._prevStatus != value:
            if bool(value):
                self._em.register(EventManager.E_NODE_ADDED, self.onNodeAdded)
                self._em.register(EventManager.E_NODE_REMOVED, self.onNodeRemoved)
                self._em.register(EventManager.E_NODE_LINKED, self.onNodeLinked)
                self._em.register(EventManager.E_NODE_UNLINKED, self.onNodeUnlinked)
                self._em.register(EventManager.E_NETWORK_READY, self.onNetworkReady)
                self._em.register(EventManager.E_NETWORK_SHUTDOWN, self.onNetworkShutdown)
                # ho bisogno di costruire la rete creata fino a questo punto
                self._browseCreatedNetwork(rete)
            else:
                self._em.unregister(EventManager.E_NODE_ADDED, self.onNodeAdded)
                self._em.unregister(EventManager.E_NODE_REMOVED, self.onNodeRemoved)
                self._em.unregister(EventManager.E_NODE_LINKED, self.onNodeLinked)
                self._em.unregister(EventManager.E_NODE_UNLINKED, self.onNodeUnlinked)
                self._em.unregister(EventManager.E_NETWORK_READY, self.onNetworkReady)
                self._em.unregister(EventManager.E_NETWORK_SHUTDOWN, self.onNetworkShutdown)
                try:
                    self._gWrapper.clear()
                except:
                    pass
                finally:    
                    self._gWrapper = None


    def onNodeAdded(self, node):
        self._gWrapper.add_node(node)
        
    def onNodeRemoved(self, node):
        #self._gWrapper.remove_node(node)
        pass
    
    def onNodeLinked(self, node, parent, linkType=0, *args):
        self._gWrapper.add_edge(parent, node, linkType)
        
    def onNodeUnlinked(self, node, parent):
        #self._gWrapper.remove_edge(node, parent)
        pass

    def onNetworkReady(self, *args):
        try:
            self._gWrapper.draw()
        except Exception, e:
            import sys
            print >> sys.stderr, "Impossibile visualizzare il grafico: ", repr(e)
            
    def onNetworkShutdown(self, *args):
        try:
            self._gWrapper.clear()
        except:
            pass
        
    def _browseCreatedNetwork(self, rete):
        self._gWrapper = NetworkXGraphWrapper.i()
        from icse.rete.ReteNetwork import ReteNetwork
        from icse.rete.Nodes import ReteNode
        assert isinstance(rete, ReteNetwork)
        nodeQueue = [(rete.get_root(), None, 0)]
        readed_saw = set()
        readed_exploded = set( )
        while len(nodeQueue) > 0:
            node, parent, linkType = nodeQueue.pop(0)
            if node not in readed_saw:
                readed_saw.add(node)
                EventManager.trigger(EventManager.E_NODE_ADDED, node)
            if parent != None:
                EventManager.trigger(EventManager.E_NODE_LINKED, node, parent, linkType)
                
            if node not in readed_exploded:
                readed_exploded.add(node)
                # per AlphaRoot, ConstantTestNode, LengthTestNode e ReteNode
                if hasattr(node, 'get_children'):
                    linkType = -1 if isinstance(node, ReteNode) else 0
                    for succ in node.get_children():
                        nodeQueue.append( (succ, node, linkType ) )
                # per ConstantTestNode, JoinNode e NegativeNode
                if hasattr(node, 'get_alphamemory'):
                    if not isinstance(node, ReteNode):
                        if node.get_alphamemory() != None:
                            nodeQueue.append( (node.get_alphamemory(), node, 0 ) )
                # per AlphaMemory
                if hasattr(node, 'get_successors'):
                    for succ in node.get_successors():
                        linkType = 1 if isinstance(succ, ReteNode) else 0
                        nodeQueue.append( (succ, node, linkType ) )
                if hasattr(node, 'get_partner'):
                    nodeQueue.append( (node.get_partner(), node, 0 ) )
        
            
class EventManager(object):
    
    E_RULE_FIRED = 'rule-fired'
    E_RULE_ACTIVATED = 'rule-activated'
    E_RULE_DEACTIVATED = 'rule-deactivated'
    E_RULE_ADDED = 'rule-added'
    E_RULE_REMOVED = 'rule-removed'
    
    E_NODE_ADDED = 'node-added'
    E_NODE_REMOVED = 'node-removed' 
    E_NODE_LINKED = 'node-linked'
    E_NODE_UNLINKED = 'node-unlinked'
    E_NODE_ACTIVATED = 'node-activated'

    E_FACT_ASSERTED = 'fact-asserted'
    E_FACT_RETRACTD = 'fact-retractd'
    
    E_ACTION_PERFORMED = 'action-performed'
    
    E_STRATEGY_CHANGED = 'strategy-changed'

    E_DEBUG_OPTIONS_CHANGED = 'debug-options-changed'
    
    E_MODULE_INCLUDED = 'module-included'
    
    E_NETWORK_READY = 'network-ready'
    E_NETWORK_SHUTDOWN = 'network-shutdown'
    
    __observers = {}
    
    @staticmethod
    def trigger(event, *args ):
        if EventManager.__observers.has_key(event):
            for observer in EventManager.__observers[event]:
                observer(*args)
                
    @staticmethod
    def register(event, handler):
        if not EventManager.__observers.has_key(event):
            EventManager.__observers[event] = set()
        if handler not in EventManager.__observers[event]: 
            EventManager.__observers[event].add(handler)

    @staticmethod
    def unregister(event, handler):
        try:
            EventManager.__observers[event].remove(handler)
        except:
            # handler non era registrato
            pass
            
    @staticmethod
    def isRegistered(event, handler):
        try:
            return (handler in EventManager.__observers[event])
        except:
            return False
        
    @staticmethod
    def reset():
        EventManager.__observers = {}
