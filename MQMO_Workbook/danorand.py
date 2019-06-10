import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import numpy as np

def sorted_poisson_arrival(lambd, t_end):
    event_times = np.random.uniform(low=0,high=t_end,size=np.int(t_end*lambd))
    event_times = np.sort(event_times)
    return event_times

def possibility_for_num_of_events_in_time(event_times, how_many_events, t_end, t_observed):
    # Number of time-intervals to check for
    # 200'000 * 0.5h
    num_observed_intervals = np.int(t_end*(1/t_observed))

    # Histogram with bins for each half hour
    # 1. 0.5h -> 3 Autos, 2. 0.5h -> 1 Auto, etc. ....
    hist, bins = np.histogram(event_times, bins=num_observed_intervals)

    # Number of histogram bins with the same count as our observed number of events
    num_events_in_observed = np.sum(hist == how_many_events)
    return num_events_in_observed/num_observed_intervals

def exp_rnd_lambd(lambd, size=None):
    return np.random.exponential(scale=1/lambd,size=size)

def exp_rnd_avg(avg, size=None):
    return np.random.exponential(scale=avg, size=size)