import json
import os
import re
import sys


def stitch(path, fn_stitched):

    samples = []

    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isdir(p):

            # Get the toplevel params.
            parameters_json_fn = os.path.join(p, 'parameters.json')
            assert os.path.isfile(parameters_json_fn)
            f = open(parameters_json_fn)
            params = json.loads(f.read())
            f.close()

            for q in os.listdir(p):
                q = os.path.join(p, q)
                if os.path.isdir(q):

                    # Swizzle together all params.

                    derived_params_json_fn = os.path.join(q, 'derived_params.json')
                    assert os.path.isfile(derived_params_json_fn)
                    f = open(derived_params_json_fn)
                    derived_params = json.loads(f.read())
                    f.close()

                    assert all(map(lambda k: k not in derived_params, params))
                    derived_params.update(params)

                    # Load the data itself.

                    data_fn = os.path.join(q, 'the.data')
                    assert os.path.isfile(data_fn)
                    f = open(data_fn)
                    for line in f:
                        cols = re.split(r'\s+', line)
                        assert len(cols) == 6

                        # Each row is a sample.
                        sample = dict(derived_params)
                        sample['frequency'] = cols[1]
                        sample['gain'] = cols[2]
                        sample['phase'] = cols[4]
                        samples.append(sample)


    # Order the first row's keys, that's the ordering for the rest of
    # the data.
    key_order = sorted(samples[0].keys())
    f = open(fn_stitched, 'w')
    print >> f, '\t'.join(key_order)
    for s in samples:
        print >> f, '\t'.join([str(s[k]) for k in key_order])
    f.close()


if __name__ == '__main__':
    assert len(sys.argv) == 2
    stitch(sys.argv[1])
