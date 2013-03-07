import csv
import os.path
import pprint
import sys
import unittest

import insert_scine
import model.simple
import progression
import the_platform


def run(fn):
    # Build up experimental samples.
    print 'reading from %s..' % fn
    f = open(fn)
    c = csv.reader(f)
    samples = [{}]
    try:
        for row in c:
            if row[0][0] == '#':
                continue

            if len(row) == 5:
                name, start, stop, points, sampling = row
                if sampling == '0':
                    progress = progression.Linear
                elif sampling == '1':
                    progress = progression.Logarithmic
                else:
                    raise Exception('sampling == "%s"' % sampling)
                progress = progress(float(start), float(stop), int(points))

            elif len(row) == 2:
                name, constant = row
                progress = progression.Constant(float(constant))

            else:
                raise Exception('CSV format borked -- len(row) = %i, row = %s' % (len(row), row))

            try:
                new_samples = []
                while True:
                    v = progress.next()
                    for sample in samples:
                        sample = dict(sample)
                        sample[name] = v
                        new_samples.append(sample)
            except StopIteration:
                samples = new_samples
    except StopIteration:
        pass

    # For all samples,
    pp = pprint.PrettyPrinter(indent=4)
    root = the_platform._root
    for i, sample in enumerate(samples):
        the_platform.set_root(os.path.join(*(root + ['trial=%i' % i])))

        # store the params to be used in the simulation,
        f = open(the_platform.file('parameters.json'), 'w')
        f.write(pp.pformat(sample))
        f.close()

        # and run the simulation.
        print sample
        insert_scine.insert_scine(model.simple, **sample)


if __name__ == '__main__':
    assert len(sys.argv) == 2
    _, csv_fn = sys.argv
    run(csv_fn)
