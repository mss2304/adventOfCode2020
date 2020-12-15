#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 06:00:31 2020

@author: marc
"""

import numpy as np
from scipy import sparse
from sys import getsizeof

inp = [6,3,15,13,1,0]
N = 30000000
M = N//8
nrs = -1*np.ones(M, dtype=int)
nrs[:len(inp)] = inp
lastoc = -1*np.ones(M, dtype=int)
lastoc[:len(inp)] = range(len(inp))
seclastoc = -1*np.ones(M, dtype=int)
curpos = len(inp)
curnr = nrs[curpos-1]
cidx = curpos+1
# this is crucial: store positions in a list; otherwise we spend an eternity searching for them!
#pos = sparse.lil_matrix((1,N), dtype=int)  # sparse array saves a lot of memory, but normal np array is faster!
pos = -1*np.ones(N, dtype=int)

for k,i in enumerate(inp):  # write position of the initial elements
#    pos[0,i] = k
    pos[i] = k

for i in range(len(inp), N):   
    if (seclastoc[cidx] == -1): # spoken the first time
        curnr = 0
    else:
        curnr = lastoc[cidx] - seclastoc[cidx]
    
    if ((i+1) % 500000 == 0):
        print(f"Turn {i+1}: curnr = {curnr}, at array pos {curpos} out of {M}")
        
#    residx = pos[0,curnr]
    residx = pos[curnr]
    
    if (residx != -1): # res is already present
        cidx = residx
        seclastoc[cidx] = lastoc[cidx]
        lastoc[cidx] = i
    else:               # res is not yet present
        nrs[curpos] = curnr
#        pos[0,curnr] = curpos  # save position of new element!
        pos[curnr] = curpos
        lastoc[curpos] = i
        curpos += 1
        cidx = curpos
        
print(f"Task 1/2: The {N}th number spoken is {curnr}.")
print(f"Memory usage [MiB]: nrs, lastoc, seclastocc: {getsizeof(nrs)//1024**2}, pos: {getsizeof(pos)//1024**2}")
    
    