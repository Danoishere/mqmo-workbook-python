import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import danorand as dr
import danolin as dl
import numpy as np
import matplotlib.pyplot as plt
import pulp as pp



# Price-matrix
# Row = From
# Column = To
P = np.array([[3,2,7,6],
              [7,5,2,3],
              [2,5,4,5]])

row_sums = np.array([5000, 6000, 2500])
column_sums = np.array([6000, 4000, 2000, 1500])

prob = pp.LpProblem("My LP Problem", pp.LpMinimize)

# solution matrix in the shape of P
x = dl.create_pulp_matrix2d(P.shape)

# Minimize number of transportation
prob += pp.lpSum(dl.multiply_vec(P.flatten(), x.flatten())), "Transport cash"

dl.column_sum_constraints(prob, x, column_sums)
dl.row_sum_constraints(prob, x, row_sums)

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
