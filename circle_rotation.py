from PIL import Image
import os

print('Program started!')

# Пути к директориям
current_dir = os.getcwd()
inner_arch_folder = os.path.join(current_dir, 'inner_archs')
external_arch_folder = os.path.join(current_dir, 'external_archs')
output_folder = os.path.join(current_dir, 'output')

# Параметры окружности и внутренних кругов
num_segments = 12
rotation_angle = (360 // num_segments)  # Угол поворота в градусах
rotation_steps = num_segments  # Количество поворотов для каждого круга

inner_circle_files = os.listdir(inner_arch_folder)
external_circle_files = os.listdir(external_arch_folder)

for external_circle_file in external_circle_files:
    if external_circle_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        external_circle_path = os.path.join(external_arch_folder, external_circle_file)
        external_circle = Image.open(external_circle_path)
        for inner_circle_file in inner_circle_files:
            if inner_circle_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                inner_circle_path = os.path.join(inner_arch_folder, inner_circle_file)
                inner_circle = Image.open(inner_circle_path)

                # Создание папки с перебором
                inner_parts = inner_circle_file.split('.')
                external_parts = external_circle_file.split('.')
                if f'external_{external_parts[0]}' not in os.listdir(output_folder):
                    os.mkdir(f'{output_folder}/external_{external_parts[0]}')
                # extra_output_folder = os.

                # Поворот и сохранение изображений
                for step in range(rotation_steps):
                    angle = step * rotation_angle
                    rotated_circle = inner_circle.rotate(angle, expand=False, resample=Image.BICUBIC)

                    # Наложение внешних дуг на внутренние
                    result_image = Image.new('RGBA', rotated_circle.size)
                    result_image.paste(rotated_circle, (0, 0))

                    # Наложение внешних дуг на внутренние с учетом альфа-канала
                    result_image.paste(external_circle, (0, 0), external_circle)

                    # Название и сохранение
                    new_filename = f'circle_e{external_parts[0]}_i{inner_parts[0]}_s{step}.png'
                    output_path = os.path.join(f'{output_folder}/external_{external_parts[0]}', new_filename)
                    result_image.save(output_path)


print('Done!')
