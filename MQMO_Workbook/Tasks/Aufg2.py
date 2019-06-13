import pyximport; pyximport.install()
import simpyx as sp
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool as ThreadPool 
import numpy as np
import danosim as ds
import danorand as dr
import danolin as dl
from numpy.random import choice

def experiment(seats):
    print('-Start-')
    env = sp.Environment();
    ticks_per_experiment = 8*60
    env.ticks = 500000

    q = ds.new_queue(env, size=seats)
    ds.poisson_arrival(env, q, arrival_rate=0.3)
    s1 = ds.server(env, q, serving_delay=2)
    #ds.status(env, 10000)
    env.run(until=env.ticks)

    num_of_experiments = env.ticks/ticks_per_experiment
    avg_num_served = s1.num_served/num_of_experiments

    print('Avg. num served: ' + str(avg_num_served))

    profit = -seats * 20
    profit += avg_num_served*15
    profit = profit/ticks_per_experiment
    print('-Stop-')

    return seats, profit

def run():
    seats = np.arange(1,10+1)
    result = ds.run_many(experiment, seats)
    x = result[:,0]
    y = result[:,1]
    plt.plot(x,y)
    plt.show()


if __name__ == '__main__':
    run()

    