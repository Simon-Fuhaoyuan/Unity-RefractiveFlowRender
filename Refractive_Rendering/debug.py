import os
from tqdm import tqdm
import random
import argparse


PREFIX = '/disk1/data/haoyuan/TOM-Net_Povray_Inc_Objects/'

# options
OUT_DIRS = ['Images_Glass/', 'Images_Lens/', 'Images_Complex/', 'Images/']
CATEGORIES = ['Glass/', 'Lens/', 'Complex/', 'Glass/']
FILES = ['train_glass_obj.txt', 'train_lens_obj.txt', 'train_complex_obj.txt', 'train_glass_obj.txt']
COUNTER = ['counter_glass', 'counter_lens', 'counter_complex', 'counter_debug']
SETTINGS = ['setting_glass.pov', 'setting_lens.pov', 'setting_complex.pov', 'setting_debug.pov']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', default='0')
    args = parser.parse_args()

    return args

def update_counter(cnt):
    with open(counter_file, 'w') as f:
        f.write(str(cnt))

def set_environ(mode):
    objects_list_file = FILES[mode]
    objects_path_prefix = PREFIX + CATEGORIES[mode]
    counter_file = COUNTER[mode]

    os.putenv('objects_prefix', objects_path_prefix)
    os.putenv('outDir', OUT_DIRS[mode])
    os.putenv('setting', os.path.join('./data/', SETTINGS[mode]))

    return objects_list_file, counter_file

def generate(objects_list_file, counter_file):
    os.putenv('obj', '0001')
    os.system('sh debug_render.sh')
        

if __name__ == '__main__':
    args = parse_args()
    objects_list_file, counter_file = set_environ(int(args.mode))
    generate(objects_list_file, counter_file)
    
