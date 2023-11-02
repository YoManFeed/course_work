import copy
from settings import *
from icecream import ic


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


def block(code: list[int]) -> list[str]:
    code = ''.join(list(map(str, code)))
    value = int(code[0])
    cur_index = 0
    blocks = []
    while cur_index < arches - 1:
        try:
            blocks.append(code[cur_index: 2 * value + cur_index])
            cur_index = 2 * value + cur_index
            value = int(code[cur_index])
        except IndexError:
            blocks.append(code[cur_index:])
            value = arches
    return blocks[:-1]


def shift(lst: list[str], step: int) -> list[str]:
    current = copy.deepcopy(lst)
    return current[step:] + current[:step]


def remove_repeated(codes: list[list[str]]) -> list[list[str]]:
    non_repeated = []
    to_check = []
    flag = True

    for blocks in codes:
        current = copy.deepcopy(blocks)

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

if __name__ == '__main__':
    pass
