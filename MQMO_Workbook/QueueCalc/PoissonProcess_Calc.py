import numpy as np
import scipy.stats as scp

t_base = 1
poissonpdf = lambda k,lmbd: np.exp(-lmbd)*lmbd**k/np.math.factorial(k)

##################################
# WSK, dass ein auto durchfährt
how_many_events = 1
# Rate = 5 Autos/h oder 2.5 Autos/30min
events_per_time = 5

# Which portion of the base-time should be observed?
t_observed = 0.5
##################################

lambd = events_per_time/(t_base/t_observed)

p = poissonpdf(how_many_events, lambd)
print(str(p))