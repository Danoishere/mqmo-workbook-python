# -----

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

#-------

import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import numpy as np

def experiment(seats = 1):
    print('-Start-')
    env = sp.Environment()
    ticks = 100000

    queue = ds.new_queue(env,size=1000000)
    ds.uniform_arrival(env, queue, arrival_delay=1)
    u = ds.new_queue(env)
    l = ds.new_queue(env)
    ds.split(env,queue,[u,l],[0.8,0.2])
    ds.server(env, u, serving_delay=0)
    ds.server(env, l, serving_delay=0)
    ds.status(env, ticks, 10000)
    env.run(until=ticks)

    print('served upper: ' + str(u.total_served))
    print('served lower: ' + str(l.total_served))
    
    return u.total_served, l.total_served
    
def run():
    values = np.repeat(1,5)
    result = ds.run_many(experiment, values)
    print('final avg. queue length = ' + str(np.average(result[:,0])) + ','  + str(np.average(result[:,1])))

if __name__ == '__main__':
    run()

    