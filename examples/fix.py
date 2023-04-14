import json
import sys

import antimeridian

with open(sys.argv[1]) as f:
    data = json.load(f)
fixed = antimeridian.fix_shape(data)
print(json.dumps(fixed, indent=4))
