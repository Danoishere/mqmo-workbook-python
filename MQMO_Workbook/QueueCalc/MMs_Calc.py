import numpy as np

perHour = 1
perMin = 60

hour = 1
min = 1/60

#################################################
# Tweak the values in the following section
#################################################
# λ (arriving objs per time)
# Throughput
arrivalRate = 15/perHour
# µ (Serving Rate)
servingRate = 0/perMin
# or
servingTimePerCustomer = 3*min
# Arbeitsstationen/Server
numberOfServers = 1
#################################################

s = numberOfServers
if servingRate == 0:
    servingRate = 1/servingTimePerCustomer

if servingTimePerCustomer == 0:
    servingTimePerCustomer = 1/servingRate

p = arrivalRate/(s*servingRate)

# Wsk für N = 0
pi0 = ((s*p)**s)/(np.math.factorial(s)*(1-p))
for i in range(0,s):
    pi0 = pi0 + (((s*p)**i)/np.math.factorial(i))

pi0 = 1/pi0
print(f'WSK. N = 0: {pi0:.4f}')
pi = pi0
sum = pi

# WSK für N = {i < s}
for i in range(1,s):
    pi = (((s*p)**i))/(np.math.factorial(i))*pi0
    sum = sum + pi
    sinv = 1 - sum
    print(f'WSK. N = {i}: {pi:.4f}\tWSK. N <= {i}: {sum:.4f}\tWSK. N > {i}: {sinv:.4f}')

# WSK für N = {i >= s}
for i in range(s,s+0):
    pi = (((s**s)*(p**i))/(np.math.factorial(s)))*pi0
    sum = sum + pi
    sinv = 1 - sum
    print(f'WSK. N = {i}: {pi:.4f}\tWSK. N <= {i}: {sum:.4f}\tWSK. N > {i}: {sinv:.4f}')

zeta = pi0 * ((s*p)**s/(np.math.factorial(s)*(1-p)))

print()
print(f'rho (Mittlere Auslastung): \t\t{p:.4f}')
En = s*p + (p*zeta)/(1-p)
print(f'E[N] (Erwartete Anz. im System): \t{En}')
Enq = (p*zeta)/(1-p)
print(f'E[Nq] (Anz. Kunden in Warteschlange): \t{Enq:.4f}')
Ew = 1/(servingRate - arrivalRate)
Ew_min = Ew*60
print(f'E[W] (Mittlere Durchlaufzeit):\t\t{Ew:.2f} [h]\tbzw. {Ew_min:.2f} [min]')
Ewq = (arrivalRate/(servingRate*(servingRate - arrivalRate)))
Ewq_min = Ewq *60
print(f'E[Wq] (Mittlere Wartezeit):\t\t{Ewq:.2f} [h]\tbzw. {Ewq_min:.2f} [min]')
print()
print(f'WSK., dass ein ankommender Kunde warten muss: {zeta:.2f}')