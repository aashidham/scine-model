import json
import sys


order = None

for j_fn in sys.argv[1:]:
    f = open(j_fn)
    for row in json.loads(f.read()):
        if order is None:
            order = row.keys()
            print ' '.join(order)
        print ' '.join([str(row[k]) for k in order])
    f.close()
