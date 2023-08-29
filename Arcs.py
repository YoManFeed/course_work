import numpy as np

generated_numbers = np.array([])
k = 12 # количество точек на прямой (обязательно чётное)
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

generated_numbers = f(cnt, ind, k, init) # Получили все последовательности Каталана

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

numbers = np.array([])
for number in generated_numbers:
    number = list(map(int, str(number)))
    number = np.array([-1 if elem == 0 else elem for elem in number])
    number = beautiful_number(number)
    number = np.array([0 if elem == -1 else elem for elem in number])
    number = str(''.join(map(str, number)))
    numbers = np.append(numbers, number)

output = []
for number in numbers:
    line = number[3:].split(' | ')
    line.sort()
    output.append(line)

l = []
for number in output: # Сортировка
    if number not in l:
        l.append(number)

print("Всего различных расположений:", len(l))

for number in l:
    print(*number)