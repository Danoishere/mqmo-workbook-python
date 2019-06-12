import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import danorand as dr
import danolin as dl
import numpy as np
import matplotlib.pyplot as plt
import pulp as pp


prob = pp.LpProblem("My LP Problem", pp.LpMinimize)

# Columns = Schichten
# Rows = Stunden in den Schichten

Inz = np.array([[1,0,0,0,0,1],
                [1,1,0,0,0,0],
                [0,1,1,0,0,0],
                [0,0,1,1,0,0],
                [0,0,0,1,1,0],
                [0,0,0,0,1,1]])

b = np.array([3,8,10,8,14,5])

# A*x = b

# Create x
x = dl.create_pulp_vector(Inz.shape[1])

# price per shift-hour
p = np.array([80, 75, 70, 70, 75, 80])

# hours per shift
h = np.array([8, 8, 8, 8, 8, 8])
  
# total price per shift
ptot = np.multiply(p,h)

# Prices/Target function
prob += dl.multiply_vec(ptot, x), "Cash" 

# Max. employees constraint
prob += pp.lpSum(x) <= 27

# Row-constriansts
for row in range(Inz.shape[0]):
    prob += pp.lpSum([x[column]*Inz[row,column] for column in range(Inz.shape[1])]) >= b[row] 

prob.solve()

print('Final value: ' + str(pp.value(prob.objective)))
print('Status: ' + pp.LpStatus[prob.status])
print('')
print('Constraints')
print('-----------------------------')
for condition in prob.constraints:
    print(prob.constraints[condition])

print('')
print('Values')
print('-----------------------------')
for variable in prob.variables():
    print("{} = {}".format(variable.name, variable.varValue))
