# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 01:00:54 2019

@author: Lenovo
"""

from gurobipy import *

 # Model data

nodes,supply=multidict({
        3:0,4:0,
        5:0,6:0,
        7:0,8:0,
        9:0,10:0})
 
arcs, upcap = multidict({
    (1, 3):  83,
    (1, 4):  72,
    (1, 5):  65,
    (2, 4):  84,
    (2, 5):  77,
    (3, 6):  69,
    (3, 7):  45,
    (4, 6):  39,
    (4, 7):  83,
    (5, 6):  91,
    (5, 7):  68,
    (6, 8):  49,
    (6, 9):  52,
    (7, 8):  72,
    (7, 9):  37,
    (7, 10): 81,
    (8, 11): 82,
    (9, 11): 103,
    (10, 11):97                
    })

     
 # Create optimization model
 
m = Model('MaxSupplyNetwork')
 
 # Create variables
 
flow = m.addVars(arcs, name="flow")
 
# Flow balance constraints

m.addConstrs(
         (flow.sum(i, '*') - flow.sum('*', i) == 0 for i in nodes[2:10]), "supply")
 
# Upper arc capacity constraints

m.addConstrs(
         (flow[i, j] <= upcap[i, j] for i, j in arcs), "upCap")


#Setting objective function




 
#m.setObjective 

m.setObjective(flow[8,11]+flow[9,11]+flow[10,11], GRB.MAXIMIZE) 

m.ModelSense=GRB.MAXIMIZE


# Compute optimal solution

m.optimize()
 
# Print solution
 
print('\nVariable Information Including Sensitivity Information:\n')

for v in m.getVars():
    print("%s %s %8.2f %s %8.2f %s %8.2f %s %8.2f" % 
              (v.Varname, "=", v.X, ", reduced cost = ", abs(v.RC), ", from coeff = ", v.SAObjLow, "to coeff = ", v.SAObjUp))
    print(" ")
        
        
print('\nOptimal objective value: %g' % m.objVal)

print('\nOptimal shadow prices:\n')
for c in m.getConstrs():
        print("%s %s %8.2f %s %8.2f %s %8.2f" % (c.ConstrName, ": shadow price = ", c.Pi, ", from RHS = ", c.SARHSLow, "to RHS = ", c.SARHSUp))
        print(" ")