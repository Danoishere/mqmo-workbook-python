import pulp as pp
import numpy as np

def multiply_vec(p,x):
    return pp.lpSum([x[i]*p[i] for i in range(p.shape[0])])

prob = pp.LpProblem("My LP Problem", pp.LpMinimize)

Inz = np.array([[1, 0,	1,	0,	0,	0,	0],
                [1,	1,	1,	1,	0,	0,	0],
                [1,	1,	1,	1,	1,	0,	0],
                [0,	1,	1,	1,	1,	1,	0],
                [1,	0,	0,	1,	1,	1,	1],
                [1,	1,	0,	0,	1,	1,	1],
                [1,	1,	0,	0,	0,	1,	1],
                [0,	1,	0,	0,	0,	0,	1]])

b = np.array([7, 7, 8, 9, 10, 10, 8, 4])

x = []
for i in range(Inz.shape[1]):
    x.append(pp.LpVariable('i' + str(i), lowBound=0, cat='Discrete'))

p = [60,60,40,40,40,40,40]
h = [6,6,4,4,4,4,4]

ptot = np.multiply(p,h)

# Prices/Target function
prob += multiply_vec(ptot, x), "Cash" 

# Max. employees constraint
prob += pp.lpSum(x) <= 15

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
