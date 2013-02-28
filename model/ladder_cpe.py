import math
import numpy
import os.path
import re


def generate(name, n, alpha, d_p):

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

    # Return circuit.

    cpe = ['.subckt %s in out' % name]
    cpe.append('* alpha=%s n=%s f_low=%s f_high=%s' % (alpha, n, f_low, f_high))

    i = 0
    for r, c in zip(r_k, c_k):
        cpe.append('r%s in rung_%i %s' % (i, i, r))
        cpe.append('c%s rung_%i out %s' % (i, i, c))
        i += 1

    cpe.append('rP in out %s' % r_p)
    cpe.append('cP in out %s' % c_p)
    cpe.append('.ends')

    return cpe


if __name__ == '__main__':
    import sys
    import tempfile

    filename, _ = generate(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), '')
    print filename
