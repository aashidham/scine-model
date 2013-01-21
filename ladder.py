import math

f_low = float(raw_input('f_low = '))
f_high = float(raw_input('f_high = '))
phi = float(raw_input('phi = '))
n = int(raw_input('n = '))

f = open('cpe.cir', 'w')
print >> f, '.subckt cpe in out'

r_1 = 1
c_1 = 1 / f_low
ab = pow(f_low / f_high, 1.0 / n)
a = pow(10, (phi / 90.0) * math.log(ab, 10))
b = ab / a
assert b < 1
assert a < 1

for i in range(n):
    print >> f, 'r%s in rung_%i %s' % (i, i, r_1 * pow(a, i))
    print >> f, 'c%s rung_%i out %s' % (i, i, c_1 * pow(b, i))

print >> f, 'rP in out %s' % (r_1 * ((1 - a) / a))
print >> f, 'rC in out %s' % (c_1 * (pow(b, n) / (1 - b)))

print >> f, '.ends'
