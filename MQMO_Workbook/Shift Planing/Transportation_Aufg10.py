
import numpy as np

f = np.array([3,2,7,6,7,5,2,3,2,5,4,5])

beq = np.array([5,6,2.9,6,4,2,1.5])*1000

Aeq = np.array([[1,1,1,1,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,1,1,1,1],
                [1,0,0,0,1,0,0,0,1,0,0,0],
                [0,1,0,0,0,1,0,0,0,1,0,0],
                [0,0,1,0,0,0,1,0,0,0,1,0],
                [0,0,0,1,0,0,0,1,0,0,0,1]])


vars = []
for i in range(Aeq.shape[1]):
    vars.append(pp.LpVariable('i' + str(i), lowBound=0, cat='Discrete'))

# Prices/Target function
prob += pp.lpSum(vars[0:2])*6*60 + pp.lpSum(vars[2:7])*4*70, "Cash" 

# Max. employees constraint
prob += pp.lpSum(vars) == 15

# Row-constriansts
for row in range(Inz.shape[0]):
    prob += pp.lpSum([vars[column]*Inz[row,column] for column in range(Inz.shape[1])]) >= b[row] 

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


