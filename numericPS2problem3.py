from gurobipy import *
import numpy as np
# n is the number of projects
n = 20
k = np.floor(np.log(2*n))
projects = range(1, n+1) # list [1, ..., n] 
# objective coefficients (rewards) (w)
# left-hand side (LHS) coefficients (resource consumption) (r)
# right-hand side (RHS) coefficient
 # resource budget
r = [2**(n+k+1)+ 2**(k+j)+1 for j in range(1,n+1)]
b = sum(r[j]/2 for j in range(0,n))
model = Model('problem3')
# uncomment next line for linear relaxation (continuous variables)
x = model.addVars(projects, name="x") 
# uncomment next line for binary variables
#x = model.addVars(projects, name="x", vtype=GRB.BINARY)
# uncomment next line for general integer variables
# x = model.addVars(projects, name="x", vtype=GRB.INTEGER)
# Capacity constraint
model.addConstr(quicksum(r[j-1] * x[j] for j in projects) <= b)
# Variable upper bound constraints
# Objective
obj = quicksum(r[j-1] * x[j] for j in projects)
model.setObjective(obj, GRB.MAXIMIZE)
# disable Presolve
model.setParam(GRB.Param.Presolve, 0)
# disable Heuristics
model.setParam(GRB.Param.Heuristics, 0)
# disable Cuts
model.setParam(GRB.Param.Cuts, 0)       
model.optimize()
# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')
print('Variable Information:')                 
for v in model.getVars():
    print("%s %s %8.2f" % 
              (v.Varname, "=", v.X))   
    print(" ")        
print('\nOptimal objective value: %g' % model.objVal)