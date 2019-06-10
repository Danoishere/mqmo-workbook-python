import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import numpy as np
import matplotlib.pyplot as plt


def experiment(seats = 1):
    print('-Start-')
    env = sp.Environment()
    env.ticks = 16*60*60

    q1 = ds.new_queue(env, size=1000)
    q2 = ds.new_queue(env, size=1000)
    q3 = ds.new_queue(env, size=1000)

    th = 336/16/60/60

    ds.poisson_arrival(env, q1, arrival_rate=th)

    info_s1 = ds.server(env, q1, q2,  serving_delay=120)
    info_s2 = ds.server(env, q2, q3,  serving_delay=150)
    info_s3 = ds.server(env, q3,      serving_delay=135)
 
    #x_served,y_served = ds.monitor_total_served(env, q1)
    info_q1 = ds.monitor_queuelength(env, q1)
    info_q2 = ds.monitor_queuelength(env, q2)
    info_q3 = ds.monitor_queuelength(env, q3)

    ds.status(env, 1000)
    env.run(until=env.ticks)

    print('s1: ' + str(info_s1.utilization))
    print('s2: ' + str(info_s2.utilization))
    print('s3: ' + str(info_s3.utilization))

    print('avg. num in q1: ' + str(np.average(info_q1.y)))
    print('avg. num in q2: ' + str(np.average(info_q2.y)))
    print('avg. num in q3: ' + str(np.average(info_q3.y)))

    
def run():
    experiment()

    """
    results = ds.run_many(experiment, np.arange(10))
    print('q1: ' + str(np.average(results[:,0])))
    print('q2: ' + str(np.average(results[:,1])))
    print('q3: ' + str(np.average(results[:,2])))
    """


if __name__ == '__main__':
    run()

    