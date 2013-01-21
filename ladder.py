import math

f_low = float(1e-13)
f_high = float(1e13)
phi = 15.0
n = 50

print '.subckt cpe in out'

r_1 = 1
c_1 = 1 / f_low
ab = pow(f_low / f_high, 1.0 / n)
a = pow(10, (phi / 90.0) * math.log(ab, 10))
b = ab / a
assert b < 1
assert a < 1

for i in range(n):
    print 'r%s in rung_%i %s' % (i, i, r_1 * pow(a, i))
    print 'c%s rung_%i out %s' % (i, i, c_1 * pow(b, i))

print 'rP in out %s' % (r_1 * ((1 - a) / a))
print 'rC in out %s' % (c_1 * (pow(b, n) / (1 - b)))

print '.ends'
