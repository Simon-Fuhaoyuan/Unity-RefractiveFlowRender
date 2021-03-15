import os
import random

root = './Objects'
prefix = 'Sphere_'
suffix = '.inc'

for i in range(100):
    description = ''
    description += '#declare %s%d = sphere {\n' % (prefix, i + 1)
    description += '    <0, 0, 0>, 0.7\n}'

    name = prefix + '%d' % (i + 1) + suffix
    name = os.path.join(root, name)
    with open(name, 'w') as f:
        f.write(description)
