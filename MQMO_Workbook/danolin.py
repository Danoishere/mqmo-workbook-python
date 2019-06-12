import simpyx as sp
import danosim as ds
import danorand as dr
import numpy as np
import matplotlib.pyplot as plt
import pulp as pp

def multiply_vec(p,x):
    """ Multiplies to vectors element wise"""
    return pp.lpSum([x[i]*p[i] for i in range(p.shape[0])])

def row_sum_constraints(prob, X, values):
    """ constrains the sum of Matrix-rows to be exactly the given values"""
    for i in range(len(values)):
        prob += pp.lpSum(X[i,:]) == values[i]

def column_sum_constraints(prob, X, values):
    """ constrains the sum of Matrix-columns to be exactly the given values"""
    for i in range(len(values)):
        prob += pp.lpSum(X[:,i]) == values[i]

def create_pulp_matrix2d(shape):
    x = np.empty(shape, np.object_)
    x_lin = []
    for column in range(shape[0]):
        for row in range(shape[1]):
            x[column][row] = pp.LpVariable('i' + str(column) + ' - ' + str(row), lowBound=0, cat='Discrete')
            x_lin.append(x[column][row])

    return x

def create_pulp_vector(size):
    x = np.empty(size, np.object_)
    for i in range(size):
        x[i] = pp.LpVariable('i' + str(i), lowBound=0, cat='Discrete')

    return x
