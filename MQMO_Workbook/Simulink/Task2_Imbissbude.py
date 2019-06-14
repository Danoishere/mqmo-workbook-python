import matlab.engine as ml
import numpy as np
import danolab as dl
import matplotlib.pyplot as plt

env = dl.MatlabEnv()

seats = np.arange(1,7)

min_per_day = 8*60
ticks = 100000

x = []
y = []

lost = []


for s in seats:
    
    print('seats: '+ str(s))
    profit = s*-20

    env['seats'] = s
    env.run_simulink('Task2_Imbissbude', ticks)
    served = env['num_served']
    arrived = env['num_generated']
    served = served[-1]
    arrived = arrived[-1]

    exp_per_day = ticks/min_per_day

    served = served/exp_per_day
    arrived = arrived/exp_per_day

    profit += served*15
    customers_lost = arrived - served

    x.append(s)
    y.append(profit)
    lost.append(customers_lost)

    print('Seats: ' + str(s) + ', Profit: ' + str(profit) + ' Customers lost: ' + str(customers_lost))

plt.subplot(2,1,1)
plt.plot(x,y)
plt.subplot(2,1,2)
plt.plot(x,lost)
plt.show()
