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


def check_depth(nums: list, counter, flag) -> list or int or bool:
    global counter_
    # counter_ = counter
    index2 = nums[0] * 2 - 1
    # counter_ += 1

    # ic(counter_)

    ic(nums, flag)

    if nums == [1, 0] and flag == 'cut':
        counter_ += 1

    if index2 > 2:
        # ic(nums[index1 + 1:index2])
        counter_ += 1
        check_depth(nums[1:index2], counter_, flag='cut')

    if index2 + 1 != len(nums):
        # ic(nums[index2+1:])
        counter_ = min(counter_, counter_+1)
        check_depth(nums[index2+1:], counter_-1, flag='other block')

    return counter_

# TODO FIXME доделть эту функцию, чтобы из 80 вариантов отобрать нужные 46
# def check_depth(nums: list, counter, counters) -> list or int or bool:
#     counter += 1
#     index1 = 0
#     index2 = nums[0] * 2 - 1
#
#     # ic(counter_)
#
#     if index2 - index1 > 1:
#         # ic(nums[index1 + 1:index2])
#         counters.append(counter)
#         check_depth(nums[index1+1:index2], counter, counters)
#
#     # if len(nums) == 2:
#     #     counters.append(counter)
#
#     if index2 + 1 != len(nums):
#         # ic(nums[index2+1:])
#         counters.append(counter)
#         check_depth(nums[index2+1:], counter-1, counters)
#
#
#     return counters


if __name__ == '__main__':
    numbers = [6, 3, 1, 0, 1, 0, 0, 2, 1, 0, 0, 0]
    numbers = list(map(int, '321000321000'))
    numbers = list(map(int, '310100321000'))

    # with open(ex_path) as file:
    #     for external_line in file:
    #         external_line = external_line.replace(' ', '').strip()
    #         external_line = list(map(int, external_line))
    #         # result = check_depth(external_line, counter=0, counters=[])
    #         counter_=0
    #         result = check_depth(external_line, counter=0)
    #         print("Глубина рекурсии:", result, external_line)

    counter_ = 0
    result = check_depth(numbers, counter=0, flag='other block')
    print("Глубина рекурсии:", result, numbers)

# TODO Все работает, остается только научиться генерировать 46 внешних дуг, потому что у меня неправильно
# TODO и потом надо их сохранить и генерировать + рисовать, но это просто
