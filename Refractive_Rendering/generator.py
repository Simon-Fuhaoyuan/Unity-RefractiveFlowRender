import os
from tqdm import tqdm
import random
import argparse
import copy
import time
from definition import OBJECT_DEFINITION, camera_parameters, object_parameters, COLORS


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number', '-n', type=int, default=1)
    parser.add_argument('--start', '-s', type=int, default=1)
    parser.add_argument('--object_root', default='./Objects')
    parser.add_argument('--bg_root', default='/disk1/data/coco/train2017/')
    parser.add_argument('--template_template', '-t', default='./data/new_template.pov')
    parser.add_argument('--runtime_template', default='./data/runtime_template.pov')
    parser.add_argument('--template_render', default='./template_render.sh')
    parser.add_argument('--runtime_render', default='./runtime_render.sh')
    parser.add_argument('--counter', default='counter')
    args = parser.parse_args()

    return args

def update_counter(counter_file, cnt):
    with open(counter_file, 'w') as f:
        f.write(str(cnt) + '\n')

def generate_parameter(parameter):
    if len(parameter) == 0:
        return []
    elif len(parameter) == 1:
        return parameter[0]
    else:
        return random.random() * (parameter[1] - parameter[0]) + parameter[0]

def randomize_object_parameters(object_name):
    # TODO: assign the color for each category
    parameters = copy.deepcopy(object_parameters)
    for key, value in parameters.items():
        parameters[key] = generate_parameter(value)
    
    return parameters

def randomize_camera_parameters():
    parameters = copy.deepcopy(camera_parameters)
    for key, value in parameters.items():
        parameters[key] = generate_parameter(value)
    
    return parameters

def value2str(value):
    if type(value) == float:
        return '%.2f' % value
    elif type(value) == str:
        return value
    else:
        return '~'

def get_color(name):
    category_id = name[:-4]
    category = ''
    index = 0
    while category_id[index] != '_':
        category += category_id[index]
        index += 1
    return COLORS[category]

def generate_template(args, objects_list):
    template = ''
    with open(args.template_template, 'r') as f:
        template = f.read()
    indices = random.sample(range(0, len(objects_list)), random.randint(1, 3))
    # print(indices)
    for i in range(len(indices)):
        index = indices[i]
        inc_file = os.path.join(args.object_root, objects_list[index])
        added_code = '#include \"%s\"' % inc_file
        replace_inc = '// include_file%d' % (i + 1)
        template = template.replace(replace_inc, added_code)

        parameters = randomize_object_parameters(objects_list[index])
        parameters['COLOR'] = get_color(objects_list[index])
        object_definition = copy.deepcopy(OBJECT_DEFINITION)
        object_definition = object_definition.replace('shape', objects_list[index][:-4])
        for key, value in parameters.items():
            object_definition = object_definition.replace('${' + key + '}', value2str(value))
        replace_object = '// object%d' % (i + 1)
        template = template.replace(replace_object, object_definition)
    # print(template)
    with open(args.runtime_template, 'w') as f:
        f.write(template)

def generate_shell(args, bg_list):
    template = ''
    with open(args.template_render, 'r') as f:
        template = f.read()
    parameters = randomize_camera_parameters()
    for key, value in parameters.items():
            template = template.replace('${' + key + '}', value2str(value))
    index = random.randint(0, len(bg_list) - 1)
    background = os.path.join(args.bg_root, bg_list[index])
    template = template.replace('${COCOImage}', background)
    print(template)
    with open(args.runtime_render, 'w') as f:
        f.write(template)

def generate(args):
    objects_list = os.listdir(args.object_root)
    random.shuffle(objects_list)
    backgrounds_list = os.listdir(args.bg_root)
    for i in range(args.start, args.start + args.number):
        generate_template(args, objects_list)
        generate_shell(args, backgrounds_list)
        os.putenv('obj', str(i))
        os.system('bash %s' % args.runtime_render)
        update_counter(args.counter, i)
        

if __name__ == '__main__':
    start = time.time()
    args = parse_args()
    generate(args)
    print(time.time() - start)
