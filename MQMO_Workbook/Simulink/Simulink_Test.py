import matlab.engine as ml
import numpy as np
import danolab as dl

env = dl.MatlabEnv()
env.run_simulink('MM1', 100000)
utilization = env['utilization']

queue_len,_ = env['qlen']
average_len = np.average(queue_len)

print(str(average_len))