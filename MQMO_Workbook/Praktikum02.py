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

def hist_queue_length(queue, timeinterval):
    hist, bins = np.histogram(queue.queuelength.x,bins=10)
    plt.h
    return len(queue.items) == 0

def new_queue(env, size=float('inf')):
    queue = sp.Store(env, capacity=size)
    queue.total = 0
    queue.total_served = 0
    queue.total_refused = 0

    queue.queuelength = Object()
    queue.queuelength.x = []
    queue.queuelength.y = []

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
        queue.queuelength.x.append(env.now)
        queue.queuelength.y.append(len(queue.items))

def status(env, end, samplingdelay = 10000):
    while True:
        print(str(env.now) + '/' + str(end))
        yield env.timeout(samplingdelay)

def experiment():
    print('-Start-')
    env = sp.Environment();
    ticks_per_experiment = 100
    ticks = 50000

    queue = new_queue(env)
    env.process(arrival(env, queue, arrival_rate=4))
    env.process(server(env, queue, serving_delay=0.2))
    env.process(monitor_queuelength(env, queue, 10))
    env.process(status(env, ticks))
    env.run(until=ticks)
    
    print('-Stop-')
    plt.plot(queue.queuelength.x, queue.queuelength.y)
    plt.show()

if __name__ == '__main__':
    experiment()

    