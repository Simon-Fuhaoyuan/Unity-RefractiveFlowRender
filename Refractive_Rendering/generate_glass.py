import os
import random

root = './Objects'
prefix = 'Glass_'
suffix = '.inc'

for i in range(100):
    description = ''
    description += '#declare %s%d = box {\n' % (prefix, i + 1)
    parameters = []
    for j in range(2):
        parameters.append(random.random() * 0.8 + 0.05)
    parameters.append(random.random() * 0.05 + 0.03)
    description += '    <-%.2f, -%.2f, -%.2f>,\n    <%.2f, %.2f, %.2f>\n}' % (parameters[0], parameters[1], parameters[2], parameters[0], parameters[1], parameters[2])

    name = prefix + '%d' % (i + 1) + suffix
    name = os.path.join(root, name)
    with open(name, 'w') as f:
        f.write(description)
