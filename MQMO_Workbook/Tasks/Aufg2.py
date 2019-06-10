import pyximport; pyximport.install()
import simpyx as sp
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool as ThreadPool 
import numpy as np
from numpy.random import choice

class Object(object):
    pass

def is_queue_full(queue):
    return len(queue.items) >= queue.capacity

def is_queue_empty(queue):
    return len(queue.items) == 0

def new_queue(env, size=float('inf')):
    queue = sp.Store(env, capacity=size)
    queue.total = 0
    queue.total_served = 0
    queue.total_refused = 0
    queue.stats = Object()
    queue.stats.x = []
    queue.stats.y = []
    return queue

def exp_rnd(avg):
    return np.random.exponential(scale=avg)

def arrival(env,queue, arrival_rate = -1, arrival_delay = -1):
    if arrival_rate != -1:
        arrival_delay = 1/arrival_rate

    while True:
        client = Object()
        queue.total = queue.total + 1
        if is_queue_full(queue):
            queue.total_refused = queue.total_refused + 1
        else:
            yield queue.put(client)

        yield env.timeout(exp_rnd(arrival_delay))

def split(env, from_queue, queues, probabilities):
    while True:
        forward_queue = choice(queues, 1, p=probabilities)[0]
        item = yield from_queue.get()
        yield forward_queue.put(item)

def server(env,from_queue, to_queue=None, serving_rate = -1, serving_delay = -1):
    """ takes an element from the from_queue, waits a given delay and forwards it
    to the to_queue"""

    if serving_rate != -1:
        serving_delay = 1/serving_rate

    while True:
        client = yield from_queue.get()
        yield env.timeout(exp_rnd(serving_delay))
        if to_queue is not None:
            if is_queue_full(to_queue):
                to_queue.total_refused = to_queue.total_refused + 1
            else:
                yield to_queue.put(client)

        from_queue.total_served = from_queue.total_served + 1

def monitor_queuelength(env, queue, samplingdelay = 1000):
    while True:
        yield env.timeout(samplingdelay)
        queue.stats.x.append(env.now)
        queue.stats.y.append(len(queue.items))

def status(env, end, samplingdelay = 10000):
    while True:
        #print(str(env.now) + '/' + str(end))
        yield env.timeout(samplingdelay)

def experiment(seats):
    print('-Start-')
    env = sp.Environment();
    ticks_per_experiment = 8*60
    ticks = 500000

    queue1 = new_queue(env, size=seats)
    #queue2 = new_queue(env, size=seats)

    #env.process(split(env, entrance, [queue1,queue2],[0.3,0.7]))
    env.process(arrival(env, queue1, arrival_rate=0.3))
    env.process(server(env, queue1, serving_delay=2))
    #env.process(server(env, queue2, serving_delay=2))
    env.process(status(env, ticks))
    env.run(until=ticks)

    num_of_experiments = ticks/ticks_per_experiment
    avg_num_served = queue1.total_served/num_of_experiments

    profit = -seats * 20
    profit += avg_num_served*15
    profit = profit/ticks_per_experiment
    print('-Stop-')
    return seats, profit

def run():
    num_of_values = 20
    pool = ThreadPool(12) 
    values = np.arange(1,num_of_values+1,1)
    results = pool.map(experiment, values)
    pool.close() 
    pool.join() 

    x = []
    y = []

    for r in results:
        x.append(r[0])
        y.append(r[1])

    plt.plot(x,y)
    plt.show()


if __name__ == '__main__':
    run()

    