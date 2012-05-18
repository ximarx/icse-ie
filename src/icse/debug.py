'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''

from icse.rete.Token import Token
from icse.rete.WME import WME
from icse.rete.Nodes import AlphaMemory, AlphaRootNode

def show_wme_details(wme, indent=4, explodeToken=False, maxDepth=3, explodeAMem=False):

    
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
    
    
    