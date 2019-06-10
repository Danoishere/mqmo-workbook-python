import numpy as np

t_end = 1000000
t_time = 1

# Simulate poisson processes (independent arrival times)
# Aufg. 1 Aufgabensammlung
#--------------------------

##############################
# 5 cars/h
events_per_time = 5

# observe 30min of the hour
t_observed = 0.5

# possibility for how many events in this range
how_many_events = 2

# The proportions of t_time and t_observed are important! Not its absolute size
##############################

event_times = np.random.uniform(low=0,high=t_end,size=t_end*events_per_time)
event_times = np.sort(event_times)

# Number of time-intervals to check for
# 200'000 * 0.5h
num_observed_intervals = np.int(t_end*(t_time/t_observed))

# Histogram with bins for each half hour
# 1. 0.5h -> 3 Autos, 2. 0.5h -> 1 Auto, etc. ....
hist, bins = np.histogram(event_times,bins=num_observed_intervals)

# Number of histogram bins with the same count as our observed number of events
num_events_in_observed = np.sum(hist == how_many_events)
posibility = num_events_in_observed/num_observed_intervals

print('Events per time: ' + str(events_per_time))
print('Time: ' + str(t_time))
print('Possibility for ' + str(how_many_events) + ' events in '+ str(t_observed) + ' : ' + str(posibility))
