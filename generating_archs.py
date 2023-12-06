import copy
from settings import *
from icecream import ic
from math import copysign

def stop():
    ans = input()
    if ans == 'yes':
        return False
    elif ans == 'no':
        return True
    else:
        print('incorrect command')
        stop()


def catalan(cnt: int, ind: int, arches: int, init: np.ndarray) -> np.ndarray:
    global generated_numbers
    if cnt <= arches-ind-2:
        init[ind] = '1'
        catalan(cnt+1, ind+1, arches, init)
    if cnt > 0:
        init[ind] = '0'
        catalan(cnt-1, ind+1, arches, init)
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
    if bool_prohibit:
        counter = 0
        for digit in code:
            if digit > 0:
                counter += 1
                if counter > border:
                    return False
            else:
                counter -= 1
        return True
    else:
        return True


def making_arches(codes: list[list[tuple]]):
    inner, external = [], []
    for indexes in codes:
        positions = [0] * arches
        for (x, y) in indexes:
            arch_len = (y - x + 1) // 2
            positions[x] = arch_len
        if external_checker(positions):
            external.append(positions)
        if not any(border < x for x in positions):
            inner.append(positions)
    return inner, external


def remove_repeated(codes: list[list[str]]) -> list[list[str]]:
    non_repeated = []

    for block in codes:
        current = np.array(list(map(int, block)))

        to_check = [np.roll(current, i) for i in range(len(current))]
        to_check = [tuple(shifted) for shifted in to_check]

        if all(elem not in non_repeated for elem in to_check):
            non_repeated.append(to_check[0])

    return non_repeated


def save_codes(codes: list, path: str) -> None:
    with open(path, mode='w') as file:
        for elem in codes:
            elem = list(map(str, elem))
            item = " ".join(elem)
            file.write("%s\n" % item)
    if bool_show_log:
        ic(path.split(sep='/')[-1][:-4])
        ic('file saved!')


def read_codes(path: str):
    output = []
    with open(path) as file:
        for line in file.readlines():
            output.append(list(map(int, line.strip().replace(' ', ''))))
    return output

def make_negatives(code: list[int]) -> list[int]:
    code = np.array(code)
    output = np.zeros_like(code)

    non_zero_indices = code.nonzero()[0]
    output[non_zero_indices] = code[non_zero_indices]
    output[2 * code[non_zero_indices] + non_zero_indices - 1] = -code[non_zero_indices]
    output = output.tolist()
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
    base = len(code1)
    for counter in range(base):
        elem1 = code1[i]
        elem2 = code2[i]
        i = i + 2 * elem2 - sign(elem2)
        i = ar_mod(i, base=base)
        elem2 = code2[i]
        elem1 = code1[i]
        i = i + 2 * elem1 - sign(elem1)
        i = ar_mod(i, base=base)
        if i == 0 and counter < -1 + base // 2:
            return False
    return True


if __name__ == '__main__':
        catalan_codes = catalan(cnt, ind, arches, init)
        save_codes(catalan_codes, catalan_path)