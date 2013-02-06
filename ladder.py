import math
import numpy
import re


def generate(alpha, d_p, path):

    n = 1000
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

    r_p *= fixup
    c_p /= fixup
    r_k = map(lambda r: r * fixup, r_k)
    c_k = map(lambda c: c / fixup, c_k)

    # Output circuit.

    path = '%s/cpe_alpha@%s_d_p@%s.cir' % (path, alpha, d_p)
    f = open(path, 'w')
    m = re.search('(\/?)([^\/]+).cir$', path)
    assert m
    name = m.group(2)
    print >> f, '.subckt ' + name + ' in out'
    print >> f, '* alpha=%s n=%s f_low=%s f_high=%s' % (alpha, n, f_low, f_high)

    i = 0
    for r, c in zip(r_k, c_k):
        print >> f, 'r%s in rung_%i %s' % (i, i, r)
        print >> f, 'c%s rung_%i out %s' % (i, i, c)
        i += 1

    print >> f, 'rP in out %s' % r_p
    print >> f, 'cP in out %s' % c_p

    print >> f, '.ends'

    return path, name
