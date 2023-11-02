from generating_archs import *
from working_with_images import read_arches, gather_arches, combining
import json
from settings import *
from icecream import ic


def stop():
    ans = input()
    if ans == 'yes':
        return False
    elif ans == 'no':
        return True
    else:
        print('incorrect command')
        stop()


if __name__ == '__main__':

    catalan_codes = catalan(cnt, ind, arches, init)

    result = list(map(catal_into_arch_indx, catalan_codes))
    result = list(map(making_arches, result))
    result = [item for item in result if item is not None]
    result = list(map(block, result))
    result = remove_repeated(result)

    save_codes(result, in_path)

    inner_arches = read_arches(quantity=inner_quantity, circle=False)
    external_arches = read_arches(quantity=external_quantity, circle=False)

    ex_counter = 0
    inn_counter = 0
    counter = 0

    with open(ex_path) as external_file:
        for external_line in external_file:
            ex_counter += 1
            counter += 1
            external_line = external_line.replace(' ', '').strip()
            external_line = list(map(int, external_line))

            with open('parameters.json', 'r') as params_file:
                parameters = json.load(params_file)

            if ex_counter > parameters.get('ex_counter', 0):
                with open(in_path) as inner_file:
                    for inner_line in inner_file:

                        # надо через мап присвоить значения интов
                        inner_line = inner_line.replace(' ', '').strip()
                        inner_line = list(map(int, inner_line))
                        ic(external_line)
                        inn_counter += 1

                        if f'external_{ex_counter}' not in os.listdir(output_folder):
                            os.mkdir(f'{output_folder}/external_{ex_counter}')
                        if f'external_{ex_counter}' not in os.listdir(f'{output_folder}_colored'):
                            os.mkdir(f'{output_folder}_colored/external_{ex_counter}')

                        inner_circle = gather_arches(code=inner_line, arches_type=inner_arches)
                        external_circle = gather_arches(code=external_line, arches_type=external_arches)

                        combining(inner_circle, external_circle, rotation_steps, inn_counter, ex_counter)
                    inn_counter = 0

                if counter % 100 == 0:
                    print('wanna continue to generate? yes/no')
                    if stop() == True:
                        parameters = {
                            'ex_counter': ex_counter,
                            'inn_counter': inn_counter,
                            'counter': counter
                        }
                        with open(json_path, 'w') as params_file:
                            json.dump(parameters, params_file)
                        break
                    else:
                        continue
