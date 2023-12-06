import numpy as np
import os


# логи и разрешения
bool_generate_again = True  # Надо ли ещё раз генерировать коды через данную степень
bool_draw_circle = True     # Надо ли рисовать круг
bool_save_codes = True      # Надо ли сохранять коды
bool_color_bgrd = False      # Надо ли красить и сохранять задний фон
bool_show_log = True        # Показывать логи
bool_save_pics = True       # Надо ли сохранять картинки
bool_prohibit = True        # Надо ли запрещать расположения
bool_labeling = True        # Надо ли писать коды на картинках

# Глобальные параметры
deg = 6
arches = deg * 2
border = deg / 2  # какие длины дуг запрещены для внутренних кодировок

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

catalan_path = os.path.join(current_dir, f'codes/catalan_codes_deg_{deg}.txt')
ex_path = os.path.join(current_dir, f'codes/external_codes_deg_{deg}.txt')
in_path = os.path.join(current_dir, f'codes/inner_codes_deg_{deg}.txt')
correct_sequence = []

# depends on what type of arches I want
try:
    all_files = os.listdir(os.path.join(current_dir, f'inner/deg_{deg}'))
    png_files = [file for file in all_files if file.endswith('.png')]
    inner_quantity = len(png_files)
except FileNotFoundError:
    raise ValueError('В папке нет картинок дуг')

try:
    all_files = os.listdir(os.path.join(current_dir, f'external/deg_{deg}'))
    png_files = [file for file in all_files if file.endswith('.png')]
    external_quantity = len(png_files)
except FileNotFoundError:
    raise ValueError("В папке нет картинок дуг")

inner_arches_paths = [''] * inner_quantity
inner_arches = [0] * inner_quantity

json_path = os.path.join(current_dir, 'parameters.json')
codes_counter = 1