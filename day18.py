#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 05:59:49 2020

@author: marc
"""

class opTree:
    def __init__(self, op):
        self.parent = None
        self.left = None
        self.right = None
        self.op = op
        
    def execute(self): # postorder traversal while executing operations
        if (self.op == None):
            print("ERROR: Empty node in tree!")
            return None
        elif (self.op in ['+', '*']): # we are an operator, i.e. not a leaf 
            l = self.left.execute()
            r = self.right.execute()
            if (self.op == '+'):
                return l + r
            else:
                return l * r
        else:               # we are a number, i.e. a leaf
            return self.op  # just return ourselves
        

with open("input-day18", 'r') as f:
    lines = list(f.read().splitlines())
    
#lines =  ["((1 + ((2) + ((1+2))) ))"]

result = 0
for l in lines:
    root = opTree(None)
    subtrees = []
    cur = root
    for c in l:
        if (c == ' '):
            continue
        
        elif (c == '('):
            while (not (cur.left == None or cur.right == None)) or (cur.parent != None): # go up to next node which has one child free
                cur = cur.parent
            subtrees.append(cur)
            cur = opTree(None)

        elif (c == ')'):
            while (cur.parent != None): # go to root of subtree
                cur = cur.parent 
            while (cur.op == None) and (cur.right == None): # This is if there is an unnecessary bracket around the expression
                cur = cur.left
            insertNode = subtrees.pop()
            cur.parent = insertNode
            if (insertNode.left == None):
                insertNode.left = cur
            else:
                insertNode.right = cur
            cur = insertNode
            
        elif (c in ['+', '*']):
            while (cur.parent != None) and ((cur.parent.op != None) if cur.parent != None else False): # go up until we find a free node
                cur = cur.parent
            if (cur.op == None):   # found a free node
                cur.op = c
            else: # reached root -> create new root and add operator there
                newroot = opTree(c)
                cur.parent = newroot
                newroot.left = cur
                cur = newroot
                if (len(subtrees) == 0): # we are in main tree
                    root = newroot

        else: # Number
            n = opTree(int(c))
            if (cur.left == None):
                n.parent = cur
                cur.left = n
            elif (cur.right == None):
                n.parent = cur
                cur.right = n
            else:
                newCur = opTree(None)
                cur.parent = newCur
                newCur.left = cur
                cur = newCur
                
    while (root.op == None) and (root.right == None): # This is if there is an unnecessary bracket around the expression
        root = root.left
        
    result += root.execute()

print(f"Task 1: Sum is {result}")