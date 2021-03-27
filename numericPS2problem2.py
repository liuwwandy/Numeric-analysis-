from gurobipy import *
m = 3 # number of operations
n = 4 # number of products
p = 4 #numeber of binary variables auxiliar
operations = range(1, m+1)  # list [1, ..., n]
products = range(1, n+1)  # list [1, ..., n]
auxiliar = range(1, p+1)  # list [1, ..., p]
# primal objective coefficients
r_coeff = [48, 55, 50, 52] 
# primal objective coefficients for the auxiliar
aux_coeff = [-1000 , -800 ,-900,-950] 
# left-hand side (LHS) coefficients (matrix A) for the operations table
A_coeff = [[2,3,6,5],[6,3,4,3],[5,6,2,7]]
# right-hand side (RHS) coefficients
b_coeff = [600, 300, 400]
# upper capacity
upcap = [50, 400/6, 75, 100]
r = {j : r_coeff[j-1] for j in products}
aux = {j : aux_coeff[j-1] for j in auxiliar}
A = {i : {j : A_coeff[i-1][j-1] for j in products} 
    for i in operations}
b = {i : b_coeff[i-1] for i in operations}
model = Model('problem2')
x = model.addVars(products, name="x") # quantity produced
#x = model.addVars(products, name="x",vtype=GRB.INTEGER)
#now we define the binary ones:
# uncomment next lines for linear relaxation (continuous variables)
y = model.addVars(auxiliar, name="y") # quantity produced
model.addConstrs((y[j] <= 1 for j in products)) #we add 
# uncomment next line for binary variables
#y = model.addVars(auxiliar, name="y", vtype=GRB.BINARY)
model.update()
# Capacity constraints
model.addConstrs((quicksum(A[i][j] * x[j] for j in products)
                           <= b[i] 
                            for i in operations))
# Variable upper bound constraints
model.addConstrs((x[j] <= upcap[j-1]*y[j] for j in products))
# Objective
obj = quicksum(r[j] * x[j] for j in products)+quicksum(aux[j] * y[j] for j in products)
model.setObjective(obj, GRB.MAXIMIZE)        
model.optimize()
# Display solution (print the name of each variable and the solution value)
 # Print solution
# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')
print('Variable Information:')                
for v in model.getVars():
    print("%s %s %8.2f" % 
              (v.Varname, "=", v.X))  
    print(" ")       
print('\nOptimal objective value: %g' % model.objVal)     
