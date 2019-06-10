import pyximport
pyximport.install()
import simpyx as sp
from multiprocessing import Pool as ThreadPool 
import numpy as np
from numpy.random import choice

class Object(object):
    pass

# BASIC QUEUE OPERATIONS  ------------------------------------------------------------

def new_queue(env, size=float('inf')):
    queue = sp.Store(env, capacity=size)
    # number of entities that tried to enter the queue
    queue.total_arrived = 0
    # number of entities that got accepted into the queue
    queue.total_enqueued = 0
    # number of entities that got taken out of this queue
    queue.total_dequeued = 0
    # number of entities that have been refused to enter this queue
    queue.total_refused = 0

    queue.total_time_spent = 0.1
    queue.avg_num_in_queue = 0

    return queue


def enqueue(queue, item):
    queue.total_arrived += 1
    if is_queue_full(queue):
        queue.total_refused += 1
        return env.timeout(0.000)
    else:
        item.t_enqueued = queue._env.now
        queue.total_enqueued += 1
        return queue.put(item)


def dequeue(queue):
    dequeue_task = queue.get()
    queue.total_dequeued += 1
    return dequeue_task

def log_dequeue(queue, item):
    item.t_dequeued = queue._env.now
    ticks = queue._env.ticks
    queue.total_time_spent += item.t_dequeued - item.t_enqueued
    queue.avg_num_in_queue = ticks/queue.total_time_spent
    pass

def is_queue_full(queue):
    return len(queue.items) >= queue.capacity


def is_queue_empty(queue):
    return len(queue.items) == 0


# ARRIVAL ------------------------------------------------------------

def poisson_arrival(env, queue, arrival_rate=-1, arrival_delay=-1):
    env.process(_arrival(env, queue, arrival_rate, arrival_delay, rnd_func = exp_rnd))


def uniform_arrival(env,queue, arrival_rate=-1, arrival_delay=-1):
    env.process(_arrival(env,queue, arrival_rate, arrival_delay, rnd_func = lambda r: np.random.uniform(0,r)))


def constant_arrival(env,queue, arrival_rate=-1, arrival_delay=-1):
    env.process(_arrival(env,queue, arrival_rate, arrival_delay, rnd_func = lambda r: r))

def _arrival(env,queue, arrival_rate=-1, arrival_delay=-1, rnd_func = None):
    if arrival_rate != -1:
        arrival_delay = 1 / arrival_rate

    if rnd_func == None:
        rnd_func = exp_rnd

    while True:
        item = Object()
        yield enqueue(queue, item)
        yield env.timeout(rnd_func(arrival_delay))

# SPLITTING ------------------------------------------------------------

def split(env, from_queue, queues, probabilities):
    env.process(_split(env, from_queue, queues, probabilities))

def _split(env, from_queue, queues, probabilities):
    while True:
        forward_queue = choice(queues, 1, p=probabilities)[0]
        item = yield dequeue(from_queue)
        log_dequeue(from_queue, item)

        yield enqueue(forward_queue, item)

def split_where_free(env, from_queue, queues):
    env.process(_split_where_free(env, from_queue, queues))

def _split_where_free(env, from_queue, queues):
    while True:
        could_place_item = False
        rand_queue_order = np.random.shuffle(queues)

        item = yield dequeue(from_queue)
        log_dequeue(from_queue, item)

        for queue in rand_queue_order:
            if not is_queue_full(queue):
                yield enqueue(queue, item)
                could_place_item = True
                break
   
# SERVER  ------------------------------------------------------------

def server(env,from_queue, to_queue=None, serving_rate=-1, serving_delay=-1, rnd_func = None):
    server_info = Object()
    server_info.num_served = 0
    env.process(_server(env,from_queue, to_queue, serving_rate, serving_delay, rnd_func, server_info))
    return server_info

def _server(env,from_queue, to_queue, serving_rate, serving_delay, rnd_func, server_info):
    """ takes an element from the from_queue, waits a given delay and forwards it
    to the to_queue"""

    if serving_rate != -1:
        serving_delay = 1 / serving_rate

    if rnd_func == None:
        rnd_func = exp_rnd

    server_info.max_served = env.ticks*(1/serving_delay)

    while True:
        item = yield dequeue(from_queue)
        log_dequeue(from_queue, item)

        yield env.timeout(rnd_func(serving_delay))
        server_info.num_served += 1
        server_info.utilization = server_info.num_served/server_info.max_served
        if to_queue is not None:
            yield enqueue(to_queue, item)


# MONITORING  ------------------------------------------------------------

def monitor_queuelength(env, queue, samplingdelay=100):
    return monitor_custom(env, queue, lambda q:len(q.items), samplingdelay)

def monitor_total_served(env, queue, samplingdelay=100):
    return monitor_custom(env, queue, lambda q:q.total_served, samplingdelay)
    
def monitor_custom(env, queue, func, samplingdelay=100):
    info = Object()
    info.x = []
    info.y = []
    env.process(_monitor_custom(env, queue, func, info, samplingdelay))
    return info

def _monitor_custom(env, queue, func, info, samplingdelay=100):
    while True:
        yield env.timeout(samplingdelay)
        info.x.append(env.now)
        info.y.append(func(queue))

def status(env,  samplingdelay=10000):
    env.process(_status(env,  samplingdelay))

def _status(env, samplingdelay):
    while True:
        print(str(env.now) + '/' + str(env.ticks))
        yield env.timeout(samplingdelay)

  
# UTILITY  ------------------------------------------------------------

def run_many(func, params):
    pool = ThreadPool(12) 
    results = pool.map(func, params)

    pool.close() 
    pool.join() 

    return np.array(results)

  
def exp_rnd(avg):
    return np.random.exponential(scale=avg)

