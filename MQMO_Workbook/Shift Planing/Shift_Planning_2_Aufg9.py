import pulp as pp
import numpy as np
import xlwings as xw

prob = pp.LpProblem("My LP Problem", pp.LpMinimize)
wb = xw.Book('Schichtplanung_Inzidenz.xlsx').sheets['Tabelle1']

Inz = np.asarray(wb.range('D4:I9').value)
b = np.asarray(wb.range('J4:J9').value)

vars = []
for i in range(Inz.shape[1]):
    vars.append(pp.LpVariable('i' + str(i), lowBound=0, cat='Discrete'))

# Prices/Target function
# There are different prices for different shifts
prob += (vars[0]+vars[-1])*8*80 + (vars[1]+vars[-2])*8*75 + pp.lpSum(vars[2:5])*8*70, "Cash" 

# Max. employees constraint
prob += pp.lpSum(vars) <= 27

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

x = np.zeros(Inz.shape[1])
i = 0

for variable in prob.variables():
    x[i] = variable.varValue
    print("{} = {}".format(variable.name, variable.varValue))
    i = i+1

belegung = Inz @ x
print('Belegung: ' + str(belegung))

