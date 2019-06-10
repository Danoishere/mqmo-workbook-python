
import pyximport
pyximport.install()
import simpyx as sp
import danosim as ds
import danorand as dr
import numpy as np
import matplotlib.pyplot as plt

t_end = 10000

# 1.1 - 1.3

events = dr.sorted_poisson_arrival(4, t_end)
diff = np.diff(events)
plt.subplot(3,1,1)
plt.hist(diff)
plt.subplot(3,1,2)
plt.hist(dr.exp_rnd_lambd(4,40000))


poss = dr.possibility_for_num_of_events_in_time(events, 3, t_end, 0.5)
print(str(poss))

# 1.4 - Hitchhikers-paradox

avg_time_between_cars = 4
events_hitchhiker = dr.sorted_poisson_arrival(1/avg_time_between_cars, 1000)
avg_diff_half = np.average(np.diff(events_hitchhiker))/2
print(str(avg_diff_half))

# 1.5 - WSK for X=k
# -> Poisson-Verteilung

x = []
y = []

for k in range(20):
    x.append(k)
    y.append(dr.possibility_for_num_of_events_in_time(events, k, t_end, 1))

plt.subplot(3,1,3)
plt.plot(x,y)
plt.show()
