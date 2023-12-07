from generating_archs import *
from working_with_images import *
import json
from settings import *
from icecream import ic
import time
import cv2
import pandas as pd


def combining(inner, external, step, inn_counter, ex_counter, external_line, inner_line):
    # angle = step * rotation_angle
    angle = step * 0
    rotated_inner = rotation(image=inner, angle=angle)
    # combining
    combination = cv2.addWeighted(external, 0.5, rotated_inner, 0.5, 0)
    gray = cv2.cvtColor(combination, cv2.COLOR_BGR2HSV)[:, :, 2]
    T = cv2.ximgproc.niBlackThreshold(gray, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=81,
                                      k=0.1, binarizationMethod=cv2.ximgproc.BINARIZATION_WOLF)
    grayb = (gray > T).astype("uint8") * 255
    dst = grayb

    # smoothing
    dst = cv2.GaussianBlur(dst, (3, 3), 0)

    # labeling
    if bool_labeling:
        upper_text = ''.join([str(num) if num < 0 else f' {num}' for num in external_line])
        bottom_text = ''.join([str(num) if num < 0 else f' {num}' for num in inner_line])
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.8
        font_color = (120, 0, 120)
        thickness = 1

        # Координаты начальной точки для текста
        org_1 = (25, 25)
        org_2 = (25, 50)
        cv2.putText(dst, upper_text, org_1, font, font_scale, font_color, thickness)
        cv2.putText(dst, bottom_text, org_2, font, font_scale, font_color, thickness)

    # saving
    if bool_save_pics:
        new_filename = f'test_output/test_e{ex_counter}_i{inn_counter}_{step}.png'
        output_path = os.path.join(current_dir, new_filename)
        data = Image.fromarray(dst)
        data.save(output_path)

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
    closed_connections_neg = []
    closed_connections =     []
    result = []
    check_ban = []

    inner = read_codes(in_path)
    external = read_codes(ex_path)

    # inner = [[2, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]]
    # external = [[5, 4, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0]]

    inner_arches = read_arches(quantity=inner_quantity, draw_circle=bool_draw_circle)
    external_arches = read_arches(quantity=external_quantity, draw_circle=False)

    for ex_counter, external_line in enumerate(external, start=1):
        for inn_counter, inner_line in enumerate(inner, start=1):
            inner_line_neg = make_negatives(inner_line)
            external_line_neg = make_negatives(external_line)

            for step in range(rotation_steps):
                shifted_inner_code = np.roll(inner_line_neg, step)
                external_line_neg = np.roll(external_line_neg, 0)

                if cyclic_check(external_line_neg, shifted_inner_code):
                    ax = axes_of_symmetry(external_line_neg)[0]

                    symmetric_check = (-1 * np.array(shifted_inner_code)[::-1]).tolist()
                    external_check = (symmetric_inner_code(inner_line_neg, ax))

                    # print(shifted_inner_code.tolist())
                    # print(symmetric_check)
                    # print(external_check)
                    # print('~' * 80)
                    if (ex_counter, shifted_inner_code.tolist()) not in result:
                        # result.append((ex_counter, shifted_inner_code.tolist()))
                        if (ex_counter, symmetric_check) not in result:
                            # result.append((ex_counter, symmetric_check))
                            if (ex_counter, external_check) not in result:
                                result.append((ex_counter, external_check))

                                # draw(external_line_neg, shifted_inner_code, step)
                        # else:
                        #     draw(external_line_neg, symmetric_check, step+100)

    print(len(result))

                    # TODO снизу написано представление |код внешних и внутренних| + |код нег внешних и нег внутренних|
                    # closed_connections_neg.append((external_line_neg.tolist(), external_line))
                    # closed_connections.append((shifted_inner_code.tolist(), np.roll(inner_line, 0).tolist()))
                    # closed_connections_neg.append((external_line_neg.tolist(), shifted_inner_code.tolist()))
                    # closed_connections.append((external_line, np.roll(inner_line, 0).tolist()))

                    # code_external = [max(0, x) for x in elem[0]]
                    # code_inner = [max(0, x) for x in elem[1]]
                    # inner_circle = gather_arches(code=code_inner, arches_type=inner_arches)
                    # external_circle = gather_arches(code=code_external, arches_type=external_arches)
                    # combining(inner_circle, external_circle, step, inn_counter, ex_counter, external_line_neg,
                    #           shifted_inner_code)

    # df = pd.DataFrame(closed_connections_neg, columns=['Column1', 'Column2'])

    # combined_lists = [pair for pair in zip(closed_connections_neg, closed_connections)]
    # df = pd.DataFrame([item for sublist in combined_lists for item in sublist], columns=['Column1', 'Column2'])

    # print(df)


    # result = []
    # check_ban = []

    # for elem in closed_connections_neg:
    #     check = (elem[0], (-1 * np.array(elem[1])[::-1]).tolist())
    #
    #     if elem not in result and check not in result:
    #         result.append(elem)
    #         print(elem)
    #     else:
    #         check_ban.append(elem)
    # print(len(result))

    # print(len(check_ban))
    # for step, elem in enumerate(check_ban):
    #     code_external = [max(0, x) for x in elem[0]]
    #     code_inner = [max(0, x) for x in elem[1]]
    #     inner_circle = gather_arches(code=code_inner, arches_type=inner_arches)
    #     external_circle = gather_arches(code=code_external, arches_type=external_arches)
    #     combining(inner_circle, external_circle, 0, step, 0, elem[0], elem[1])

