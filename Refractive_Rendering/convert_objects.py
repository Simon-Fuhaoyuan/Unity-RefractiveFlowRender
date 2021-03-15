import os
from tqdm import tqdm
import random
import shutil

ROOT = './Objects'
sub_glass = ['sor1', 'sor2', 'sor3', 'sor4', 'piecew1']
sub_glass_files = [[], [], [], [], []]

Glass_ROOT = './Primitives/Glass'
new_glass_root = './Objects/Cups'

Lens_ROOT = './Primitives/Lens'
new_lens_root = './Objects/Lens'

def select_lens():
    # Select 100 objects from ./Primitives/Lens/
    lens_objects = os.listdir(Lens_ROOT)
    for i in range(100):
        index = random.randint(0, len(lens_objects) - 1)
        name = lens_objects[index]
        del lens_objects[index]
        shutil.copy(os.path.join(Lens_ROOT, name), os.path.join(new_lens_root, name))

def select_glass():
    # Select 20 objects from each sub-category in ./Primitives/Glass, totally 50
    glass_objects = os.listdir(Glass_ROOT)
    for glass in glass_objects:
        for i in range(len(sub_glass)):
            if sub_glass[i] in glass:
                sub_glass_files[i].append(glass)
                break

    for i in range(5):
        for j in range(20):
            index = random.randint(0, len(sub_glass_files[i]) - 1)
            name = sub_glass_files[i][index]
            del sub_glass_files[i][index]
            shutil.copy(os.path.join(Glass_ROOT, name), os.path.join(new_glass_root, name))

def convert_name():
    categories = os.listdir(ROOT)
    for category in categories:
        print('Converting category %s' % category)
        path = os.path.join(ROOT, category)
        objects = os.listdir(path)
        for i in tqdm(range(len(objects))):
            object_file = os.path.join(path, objects[i])
            content = ''
            with open(object_file, 'r') as f:
                content = f.read()
            name = category + '_%d' % (i + 1)
            content = content.replace('#declare shape =', '#declare %s =' % name)
            with open(object_file, 'w') as f:
                f.write(content)
            shutil.move(object_file, os.path.join(path, name + '.inc'))


if __name__ == '__main__':
    # select_lens()
    # select_glass()
    convert_name()