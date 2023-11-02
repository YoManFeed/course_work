import numpy as np
import os


# Глобальные параметры
arches = 12
border = 3

# Для каталана
generated_numbers = np.array([])
init = list(np.zeros(arches))  # пустой список, куда будем писать последовательности
cnt = 0  # разница между 1 и 0
ind = 0  # индекс, по которому пишем число в список

rotation_steps = arches
rotation_angle = 360/rotation_steps

current_dir = os.getcwd()
output_path = os.path.join(current_dir, 'output.png')
image_path_circle = os.path.join(current_dir, 'circle.png')
image_path_transparent = os.path.join(current_dir, 'transparent.png')

output_folder = os.path.join(current_dir, 'output')

catalan_path = os.path.join(current_dir, 'catalan_codes.txt')
ex_path = os.path.join(current_dir, 'external_codes.txt')
in_path = os.path.join(current_dir, 'inner_codes.txt')
correct_sequence = []

# depends on what type of arches I want
"""переделать подсчет иннеров и экстернелов в зависимости от их количества в отдельной папке"""
inner_quantity = 3  # inner
external_quantity = 6  # external

inner_arches_paths = [''] * inner_quantity
inner_arches = [0] * inner_quantity

json_path = os.path.join(current_dir, 'parameters.json')
