import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import numpy as np
import matplotlib.pyplot as plt


def experiment(seats = 1):
    print('-Start-')
    env = sp.Environment()
    ticks = 10000

    queue = ds.new_queue(env)
    ds.poisson_arrival(env, queue, arrival_rate=10)
    ds.server(env, queue, serving_delay=1/6, rnd_func= lambda p: np.random.uniform(0, p))

    x_served,y_served = ds.monitor_total_served(env, queue)
    x_len, y_len = ds.monitor_queuelength(env, queue)

    ds.status(env, ticks, 1000)
    env.run(until=ticks)

    plt.plot(x_len, y_len)
    plt.show()
    
def run():
    experiment()

if __name__ == '__main__':
    run()

    