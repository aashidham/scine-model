import math
import numpy

phi = float(raw_input('phi = '))
n = int(raw_input('n = '))
r_1 = float(raw_input('r_1 = '))
c_1 = float(raw_input('c_1 = '))
d_p = float(raw_input('d_p = '))

f = open('cpe.cir', 'w')
print >> f, '.subckt cpe in out'

ab = 0.24 / (1 + 0.5)
a = pow(10, (phi / 90.0) * math.log(ab, 10))
b = ab / a
print 'a = %s' % a
print 'b = %s' % b

r_k = [r_1] + [r_1 * pow(a, k + 1) for k in range(n - 1)]
c_k = [c_1] + [c_1 * pow(b, k + 1) for k in range(n - 1)]
print 'r_k = %s' % r_k
print 'c_k = %s' % c_k

r_p = r_1 * ((1 - a) / a)
c_p = c_1 * pow(b, n) / (1 - b)
w_av = pow(a / b, 0.25) / (r_1 * c_1 * pow(ab, 2))
y_rungs = sum((1j * w_av * c_k[k]) / (1 + (1j * w_av * r_k[k] * c_k[k])) for k in range(n))
z_av = 1.0 / numpy.real((1.0 / r_p) + (1j * w_av * c_p) + y_rungs)
d = z_av * pow(w_av, phi / 90.0)
print 'r_p = %s, c_p = %s' % (r_p, c_p)
print 'w_av = %s' % w_av
print 'z_av = %s' % z_av
print 'd = %s' % d

fixup = d_p / d
print 'fixup = %s' % fixup

r_p *= fixup
c_p /= fixup
r_k = map(lambda r: r * fixup, r_k)
c_k = map(lambda c: c / fixup, c_k)
print 'fixed r_p = %s, c_p = %s' % (r_p, c_p)
print 'fixed r_k = %s' % r_k
print 'fixed c_k = %s' % c_k

i = 0
for r, c in zip(r_k, c_k):
    print >> f, 'r%s in rung_%i %s' % (i, i, r)
    print >> f, 'c%s rung_%i out %s' % (i, i, c)
    i += 1

print >> f, 'rP in out %s' % r_p
print >> f, 'cP in out %s' % c_p

print >> f, '.ends'
