'''
Created on 14/lug/2012

@author: Francesco Capozzo
'''

import icse.parser as clipsparser
import time
import sys

if __name__ == '__main__':
    
    nFile = sys.argv[1]

    fr = open("../tests/"+nFile, "rU")
    _complete_test = fr.read()
    
    start_time = time.time()
    clipsparser.parse(_complete_test, False)
    print time.time() - start_time, " seconds"
    