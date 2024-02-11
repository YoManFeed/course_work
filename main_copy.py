from generating_archs import *
from working_with_images import read_arches, gather_arches, combining
import json
from icecream import ic
from tqdm import tqdm


def axes_of_symmetry(code):
    axes = []
    sum = 0
    left_index = 0
    for i, digit in enumerate(code):
        sum += digit
        if sum == 0:
            axes.append((left_index + i) // 2 + 1)
            left_index = i+1
    return axes


def symmetric_inner_code(code, ax):
    code = (-1 * np.roll(code, -ax))[::-1]
    return np.roll(code, ax).tolist()


def draw(external_line_neg, shifted_inner_code, step):
    code_external = [max(0, x) for x in external_line_neg]
    code_inner = [max(0, x) for x in shifted_inner_code]
    # code_inner = [max(0, x) for x in shifted_inner_code.tolist()]
    inner_circle = gather_arches(code=code_inner, arches_type=inner_arches)
    external_circle = gather_arches(code=code_external, arches_type=external_arches)
    combining(inner_circle, external_circle, step, inn_counter, ex_counter, external_line_neg,
              shifted_inner_code)


if __name__ == '__main__':
    print(f'\
    bool_generate_again = {bool_generate_again} \n\
    bool_draw_circle = {bool_draw_circle} \n\
    bool_save_codes = {bool_save_codes} \n\
    bool_color_bgrd = {bool_color_bgrd} \n\
    bool_show_log = {bool_show_log} \n\
    bool_save_pics = {bool_save_pics} \n\
    bool_prohibit = {bool_prohibit}')

    if bool_generate_again:
        catalan_codes = catalan(cnt, ind, arches, init)
        pair_indexes = list(map(catal_into_arch_indx, catalan_codes))
        inner, external = making_arches(pair_indexes)
        inner = remove_repeated(inner)
        external = remove_repeated(external)

        if bool_save_codes:
            save_codes(inner, in_path)
            save_codes(external, ex_path)

    else:
        inner = read_codes(in_path)
        external = read_codes(ex_path)

    # read all inner_arches
    inner_arches = read_arches(quantity=inner_quantity, draw_circle=bool_draw_circle)
    external_arches = read_arches(quantity=external_quantity, draw_circle=False)

    for ex_counter, external_line in tqdm(enumerate(external, start=1), desc="Processing External", unit="lines", total=len(external)):
        with open('parameters.json', 'r') as params_file:
            parameters = json.load(params_file)

        if ex_counter > parameters.get('ex_counter', 0):
            for inn_counter, inner_line in enumerate(inner, start=1):

                if bool_save_pics and f'external_{ex_counter}' not in os.listdir(output_folder):
                    os.mkdir(f'{output_folder}/external_{ex_counter}')
                if bool_color_bgrd and bool_save_pics and (f'external_{ex_counter}' not in os.listdir(f'{output_folder}_colored')):
                    os.mkdir(f'{output_folder}_colored/external_{ex_counter}')

                inner_line_neg = make_negatives(inner_line)
                external_line_neg = make_negatives(external_line)

                for step in range(rotation_steps):
                    shifted_inner_code = np.roll(inner_line_neg, step)
                    external_line_neg = np.roll(external_line_neg, 0)
                    if cyclic_check(external_line_neg, shifted_inner_code):
                        ax = axes_of_symmetry(external_line_neg)[0]
                        symmetric_check = (-1 * np.array(shifted_inner_code)[::-1]).tolist()
                        external_check = (symmetric_inner_code(inner_line_neg, ax))
                        codes_counter += 1

                        if (ex_counter, shifted_inner_code.tolist()) not in result:
                            if (ex_counter, symmetric_check) not in result:
                                if (ex_counter, external_check) not in result:
                                    result.append((ex_counter, external_check))

                                    if bool_draw_circle:
                                        draw(external_line_neg, shifted_inner_code, step)

                        # if bool_draw_circle:
                        #     shifted_inner_code = np.roll(inner_line_neg, step)
                        #     inner_circle = gather_arches(code=inner_line, arches_type=inner_arches)
                        #     external_circle = gather_arches(code=external_line, arches_type=external_arches)
                        #     combining(inner_circle, external_circle, step, inn_counter, ex_counter, external_line_neg, shifted_inner_code)

                        with open(f"logs/log_deg_{deg}.txt", "a") as log_file:
                            log_file.write(f"E: {external_line_neg} \nI: {shifted_inner_code}\n\n")

            if ex_counter % 100 == 0 and bool_draw_circle:
                print('wanna continue to generate? yes/no')
                if stop():
                    parameters = {
                        'ex_counter': ex_counter
                    }
                    with open(json_path, 'w') as params_file:
                        json.dump(parameters, params_file)
                    break
                else:
                    continue

    with open(f"logs/log_deg_{deg}.txt", "r+") as log_file:
        content = log_file.read()
        log_file.seek(0, 0)
        log_file.write(f"Overall: {codes_counter}\n\n" + content)

