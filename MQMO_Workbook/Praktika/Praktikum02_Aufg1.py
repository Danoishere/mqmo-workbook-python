#import pyximport
#pyximport.install()

import simpyx as sp
import danosim as ds
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool as ThreadPool 
import numpy as np

def experiment(seats = 1):

    print('-Start-')
    env = sp.Environment()
    ticks = 30000
    ticks_per_experiment = 100

    queue = ds.new_queue(env)
    env.process(ds.poisson_arrival(env, queue, arrival_delay=0.25))
    env.process(ds.server(env, queue, serving_delay=0.2))
    env.process(ds.monitor_queuelength(env, queue))
    env.process(ds.status(env, ticks))
    env.run(until=ticks)

    print('avg. queue length = ' + str(np.average(queue.queuelength.y)))
    return np.average(queue.queuelength.y)

def run():
    values = np.repeat(1, 10)
    result = ds.run_many(experiment, values)
    print('final avg. queue length = ' + str(np.average(result)))

if __name__ == '__main__':
    run()