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


def making_arches(indexes: list[tuple]) -> list or None:
    positions = [0] * arches
    for (x, y) in indexes:
        arch_len = (y - x + 1) // 2
        positions[x] = arch_len
    if any(border < x for x in positions):
        return None
    else:
        return positions


# def block(code: list[int]) -> list[str]:
#     code = ''.join(list(map(str, code)))
#     value = int(code[0])
#     cur_index = 0
#     blocks = []
#     while cur_index < arches - 1:
#         try:
#             blocks.append(code[cur_index: 2 * value + cur_index])
#             cur_index = 2 * value + cur_index
#             value = int(code[cur_index])
#         except IndexError:
#             blocks.append(code[cur_index:])
#             value = arches
#     return blocks[:-1]


def block(code: list[int]) -> list[str]:
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


def save_codes(codes, path):
    with open(path, mode='w') as file:
        for elem in codes:
            elem = list(map(str, elem))
            item = " ".join(elem)
            file.write("%s\n" % item)
    ic('file saved!')

# TODO написать код, который из кодировки list[str] заменяет нули на -1, -2, -3
# TODO потом написать код, который по индексам проверяет замкнутость


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
    # code1 = [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
    # code2 = [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
    # code1 = [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
    # code2 = [2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3, 3]
    # code1 = [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
    # code2 = [1, -1, -2, -3, 3, 2, 1, -1, -2, -3, 3, 2]
    #
    # code1 = [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
    # code2 = [-1, -2, -3, 3, 2, 1, -1, -2, -3, 3, 2, 1]
    # print(cyclic_check(code1, code2))

    counter = 0
    for i in range(14):
        for j in range(14-i):
            counter +=1
            print(i+1, j+1)
    print(counter)

    pass

# [3, 2, 1, -1, -2, -3, 3, 2, 1, -1, -2, -3]
# [1, -1, -2, -3, 3, 2, 1, -1, -2, -3, 3, 2]
