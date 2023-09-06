import numpy as np
import copy

generated_numbers = np.array([])
k = 22 # количество точек на прямой (обязательно чётное)
init = list(np.zeros(k)) # пустой список, куда будем писать последовательности
cnt = 0 # разница между 1 и 0
ind = 0 # индекс, по которому пишем число в список


def f(cnt, ind, k, init):
    global generated_numbers
    # кладем 1, только если хватает места
    if (cnt <= k-ind-2):
        init[ind] = '1'
        f(cnt+1, ind+1, k, init)
    # пишем 0 можно положить всегда, если cnt > 0
    if cnt > 0:
        init[ind] = '0'
        f(cnt-1, ind+1, k, init)
    # выходим из цикла и печатаем
    if ind == k:
        if cnt == 0:
            generated_numbers = np.append(generated_numbers, ''.join(init))
    return generated_numbers


def beautiful_number(number):
    counter = 0
    new_number = []
    summ = 0
    for digit in number:
        if summ != 0:
            summ += digit
            new_number.append(digit)
        else:
            new_number.append(' | ')
            new_number.append(digit)
            summ = number[counter]
    return new_number


def shift(lst, steps):
    current = copy.deepcopy(lst)
    for i in range(1, steps+1):
        current.insert(0, current.pop())
    return current


katalan_numbers = f(cnt, ind, k, init)  # Получили все последовательности Каталана
numbers = np.array([])
output_numbers = []

for number in katalan_numbers:
    number = list(map(int, str(number)))
    number = np.array([-1 if elem == 0 else elem for elem in number])
    number = beautiful_number(number)
    number = np.array([0 if elem == -1 else elem for elem in number])
    number = str(''.join(map(str, number)))
    line = number[3:].split(' | ')
    line = list(map(int, line))
    output_numbers.append(line)


print("Всего различных расположений, без сортировки повторов:", len(output_numbers))


def output(array):
    for elem in array:
        print(*elem)

# output(output_numbers)

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

# print(final_result)
print("Всего принципиально различных расположений:", len(final_result))

# output(final_result)