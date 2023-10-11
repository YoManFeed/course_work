import copy
from settings import *


"""Returns the code of Catalan numbers"""
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


"""Gets a catalan code and splits on groups of arches"""
def spliting(number):
    counter = 0
    new_number = []
    summ = 0
    flag = True
    for digit in number:
        if summ != 0:
            summ += digit
            new_number.append(digit)
        else:
            if not flag:
                new_number.append(' | ')
                flag = False
            new_number.append(digit)
            summ = number[counter]
            flag = False
    return new_number


"""In contrast of function above this gets the array of strings
   and returns the list of lists"""
def split_the_array(katalan_numbers):
    output_numbers = []
    for number in katalan_numbers:
        number = list(map(int, str(number)))
        number = np.array([-1 if elem == 0 else elem for elem in number])
        number = spliting(number)
        number = np.array([0 if elem == -1 else elem for elem in number])
        number = str(''.join(map(str, number)))
        line = number.split(' | ')
        line = list(map(int, line))
        output_numbers.append(line)
    return output_numbers


"""Gets a list and shifts it cyclically"""
def shift(lst, steps):
    current = copy.deepcopy(lst)
    for i in range(1, steps+1):
        current.insert(0, current.pop())
    return current


"""Deletes all repeated cyclic shifted"""
def remove_repeated(output_numbers):
    final_result = []
    check = []

    for elem in output_numbers:
        current = copy.deepcopy(elem)
        if current in check:
            pass
        else:
            for i in range(len(current)):
                check.append(shift(current, i))
            final_result.append(current)
    return final_result


""" Gets the code and returns the biggest index of an arch """
def refactoring_the_code(code: str) -> list:
    code = code.replace(' ', '')
    code = code.strip()
    # ic(code)
    filling = [-1]*12
    ones = []
    # ic(len(code))
    for i in range(len(code)):
        if code[i] == '1':
            ones.append(i)
        else:
            filling[i] = i
            filling[ones[-1]] = i
            ones.pop()

    return filling


""" Берет список, в котором указаны индексы совпадающих элементов
    Первый из одинаковых элементов заменяет на длину дуги,
    второй задаёт равным нулю.

    Интерпретация: если число, то пиши дугу данной длины, если 0 - ничего"""
def making_arches(refactored_code: list) -> list:
    copied = refactored_code.copy()[::-1]
    sequence = []
    left_index = -1
    for elem in refactored_code:
        left_index += 1
        right_index = len(refactored_code) - copied.index(elem)
        difference = right_index - left_index
        sequence.append(int(difference/2))
    return sequence


def save_catalan_code(show):
    with open(catalan_path, mode='w') as f:
        catalan_numbers = catalan(cnt, ind, arches, init)  # Получили все последовательности Каталана
        output_numbers = split_the_array(catalan_numbers)
        final_result = remove_repeated(output_numbers)

        if show:
            print("Всего различных расположений, без сортировки повторов:", len(output_numbers))
            print("Всего принципиально различных расположений:", len(remove_repeated(output_numbers)))

        for elem in final_result:
            elem = list(map(str, elem))
            item = " ".join(elem)
            f.write("%s\n" % item)


def refactor_catalan_code():
    with open(catalan_path, mode='r') as f:
        for line in f.readlines():
            temp_list = refactoring_the_code(line)
            correct_sequence.append(making_arches(temp_list))
        return correct_sequence


def save_inner_and_external_codes():
    with open(ex_path, mode='w') as ex_f:
        with open(in_path, mode='w') as in_f:
            for elem in correct_sequence:
                elem = list(map(str, elem))
                item = " ".join(elem)
                ex_f.write("%s\n" % item)  # saving codes of external arches
                if not any(x in elem for x in ('4', '5', '6')):  # saving codes of inner arches
                    in_f.write("%s\n" % item)

if __name__ == '__main__':
    pass
