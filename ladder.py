import math
import numpy

alpha = float(raw_input('alpha = '))
n = 1000 #int(raw_input('n = '))
d_p = float(raw_input('d_p = '))
cpe = str(raw_input('name ='))

f_low = 1e-6
f_high = 1e12
pi = math.pi
phi = 90 * alpha
r_1 = 1 / f_low
c_1 = 1 
ab = pow(f_low / f_high, 1.0 / n)
a = pow(10, (phi / 90.0) * math.log(ab, 10))
b = ab / a

r_k = [r_1] + [r_1 * pow(a, k + 1) for k in range(n - 1)]
c_k = [c_1] + [c_1 * pow(b, k + 1) for k in range(n - 1)]

r_p = r_1 * ((1 - a) / a)
c_p = c_1 * pow(b, n) / (1 - b)

y = 1/r_p + 2 * pi * 1j * c_p + sum((1j * 2 * pi * c_k[k])/(1+1j*r_k[k]* 2 * pi * c_k[k]) for k in range (n))
z = abs(1 / y)
fixup = d_p / z
print 'fixup = %s' % fixup

r_p *= fixup
c_p /= fixup
r_k = map(lambda r: r * fixup, r_k)
c_k = map(lambda c: c / fixup, c_k)
print 'fixed r_p = %s, c_p = %s' % (r_p, c_p)
print 'fixed r_k = %s' % r_k
print 'fixed c_k = %s' % c_k

# Output circuit.

f = open('%s.cir' % cpe, 'w')
print >> f, '.subckt '+ cpe + ' in out'
print >> f, '* ' + 'alpha= ' + '%s' %alpha + ',n= ' + '%s' %n + ',flow= ' + '%s' %f_low + ',fhigh= ' + '%s' %f_high + ',D= ' + '%s' %d_p

i = 0
for r, c in zip(r_k, c_k):
    print >> f, 'r%s in rung_%i %s' % (i, i, r)
    print >> f, 'c%s rung_%i out %s' % (i, i, c)
    i += 1

print >> f, 'rP in out %s' % r_p
print >> f, 'cP in out %s' % c_p

print >> f, '.ends'
