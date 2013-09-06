import csv
import json
import os
import sys
import unittest
import subprocess

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
    root = the_platform._root
    for i, sample in enumerate(samples):
        the_platform.set_root(os.path.join(*(root + ['trial=%i' % i])))

        # store the params to be used in the simulation,
        f = open(the_platform.file('parameters.json'), 'w')
        f.write(json.dumps(sample))
        f.close()

        # and run the simulation.
        print sample
        insert_scine.insert_scine(model.simple, **sample)
    
    root = "/".join(root)
    
    #incredibly hacky, but subprocess.check_call() couldn't work with this bash command
    cmd = "~/parallel ngspice -p %s/trial={1}/t={2}/model1.cir '<' %s/trial={1}/t={2}/spice.input ::: {0..%i} ::: {0..%i}" % (root,root,len(samples),samples[0]['Nsteps'])
    f = open("para.sh","wb")
    f.write(cmd)
    f.close()
    os.system("/bin/bash ./para.sh")

    for i in range(len(samples)):
    	for j in range(int(samples[0]['Nsteps'])+1):
			mag_plot_fn = root + "/trial=%i/t=%i/plot-mag.png" % (i,j)
			phase_plot_fn = root + "/trial=%i/t=%i/plot-phase.png" % (i,j)
			data = root + "/trial=%i/t=%i/the.data" % (i,j)
			subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 1:2 with linespoints\"" % (mag_plot_fn, data), shell=True)
			subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 3:4 with linespoints\"" % (phase_plot_fn, data), shell=True)

if __name__ == '__main__':
    assert len(sys.argv) == 2
    _, csv_fn = sys.argv
    run(csv_fn)
