import copy
from settings import *
from icecream import ic
from math import copysign


def catalan(cnt: int, ind: int, arches: int, init: np.ndarray) -> np.ndarray:
    global generated_numbers
    # кладем 1, только если хватает места
    if (cnt <= arches-ind-2):
        init[ind] = '1'
        catalan(cnt+1, ind+1, arches, init)
    # пишем 0 можно положить всегда, если cnt > 0
    if cnt > 0:
        init[ind] = '0'
        catalan(cnt-1, ind+1, arches, init)
    # выходим из цикла и печатаем
    if ind == arches:
        if cnt == 0:
            generated_numbers = np.append(generated_numbers, ''.join(init))
    return generated_numbers


def catal_into_arch_indx(number: str) -> list[tuple]:
    stack_ind_1 = []
    ans = []
    for i, digit in enumerate(number):
        if digit == '1':
            stack_ind_1.append(i)
        else:
            ans.append((stack_ind_1.pop(), i))
    return ans


def external_checker(code: list[int]) -> bool:
    counter = 0
    for digit in code:
        # TODO выяснить на что заменить 3 в общем случае
        # TODO вообще надо написать функцию глубины, которая запоминает самую длинную убывающую последовательность
        if digit != 0:
            counter += 1
            if counter > 3:
                return False
        else:
            counter = 0
    return True


def making_arches(codes: list[list[tuple]]) -> list and list:
    inner, external = [], []
    for indexes in codes:
        positions = [0] * arches
        for (x, y) in indexes:
            arch_len = (y - x + 1) // 2
            positions[x] = arch_len

        if external_checker(positions):
            # ic(positions)
            external.append(positions)

        if not any(border < x for x in positions):
            inner.append(positions)

    return inner, external


def block(code: list[str]) -> list[str]:
    code = ''.join(list(map(str, code)))
    num_non_zero = 0
    num_zero = 0
    ans = ''
    output = []
    for digit in code:

        if digit == '0':
            num_zero += 1
        else:
            num_non_zero += 1
        ans = ans + digit
        if num_zero == num_non_zero:
            output.append(ans)
            ans = ''
    return output


def shift(lst: list[str], step: int) -> list[str]:
    current = copy.deepcopy(lst)
    return current[step:] + current[:step]


def remove_repeated(codes: list[list[str]]) -> list[list[str]]:
    non_repeated = []
    to_check = []
    flag = True

    for blocks in codes:
        current = list(map(int, copy.deepcopy(blocks)))

        for i in range(len(current)):
            elem = shift(current, i)
            to_check.append(elem)
            if elem in non_repeated:
                flag = False

        if flag:
            non_repeated.append(to_check[0])

        flag = True
        to_check = []

    return non_repeated


def save_codes(codes: list, path: str, show_log: bool) -> None:
    with open(path, mode='w') as file:
        for elem in codes:
            elem = list(map(str, elem))
            item = " ".join(elem)
            file.write("%s\n" % item)
    if show_log:
        ic(path.split(sep='/')[-1][:-4])
        ic('file saved!')


def read_codes(path: str):
    output = []
    with open(path) as file:
        for line in file.readlines():
            output.append(list(map(int, line.strip().replace(' ', ''))))
    return output

def make_negatives(code: list[int]) -> list[int]:
    '''
    Надо взять список из списка интов. Который надо через remove_repeated прогнать
    '''
    output = [0] * len(code)
    for i, elem in enumerate(code):
        if elem == 0:
            pass
        else:
            output[i] = elem
            output[2 * elem + i - 1] = -elem
    return output


def sign(y) -> int:
    return int(copysign(1, y))


def ar_mod(number: int, base: int):
    if number < 0:
        return number + base
    elif 0 <= number < base:
        return number
    else:
        return number - base


def cyclic_check(code1: list[int], code2: list[int]) -> bool:
    i = 0
    # elem1 = code1[i]
    # elem2 = code2[i]
    base = len(code1)
    for counter in range(base):
        elem1 = code1[i]
        elem2 = code2[i]
        # print(code1)
        # print(code2)
        # print([i for i in range(12)])
        # print(f'bottom: index {i} elem1 {elem1}, elem2 {elem2}')
        i = i + 2 * elem2 - sign(elem2)
        # print(f'bottom index {i} changed to {ar_mod(i, base=base)}')
        i = ar_mod(i, base=base)
        elem2 = code2[i]
        elem1 = code1[i]
        # print(f'upper: index {i} elem1 {elem1}, elem2 {elem2}')
        i = i + 2 * elem1 - sign(elem1)
        # print(f'upper index {i} changed to {ar_mod(i, base=base)}')
        i = ar_mod(i, base=base)
        if i == 0 and counter < -1 + base // 2:
            return False
    return True


if __name__ == '__main__':
    # catalan_codes = catalan(cnt, ind, arches, init)
    # pair_indexes = list(map(catal_into_arch_indx, catalan_codes))
    # inner, external = making_arches(pair_indexes)
    #
    # external = list(map(block, external))
    # inner = list(map(block, inner))
    #
    #
    # inner = remove_repeated(inner)
    # external = remove_repeated(external)
    # # ic(type(inner[0][0]))
    # # inner = list(map(make_negatives, inner))
    #
    # ic(inner)
    # ic(external)
    #
    # ic(len(inner))
    # ic(len(external))

    # sequence = [6, 5, 1, 0, 3, 1, 0, 1, 0, 0, 0, 0]
    # max_number = max(sequence)
    # min_number = max_number + 1
    # sub_seq_len = 0
    # for i, number in enumerate(sequence[sequence.index(max_number):-1]):
    #     if number != 0:
    #         if number <= max_number:
    #             sub_seq_len += 1
    #             if number <
    #     else:
    #         pass

    pass

# [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
# [1, -1, -2, -3, 3, 2, 1, -1, -2, -3, 3, 2]


