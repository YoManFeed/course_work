from PIL import Image
import os
import cv2
import numpy as np
import time

start = time.time()
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


"""DO NOT TOUCH, SOMEHOW IT WORKS. REGULAR cv2.imread() HAS GLITCHES"""
def read_transparent_png(img_path):
    image_4channel = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:,:,3]
    rgb_channels = image_4channel[:,:,:3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white
    return final_image.astype(np.uint8)


def coloring(image):
    start_point = (510, 510)
    fill_color = (150, 150, 255)
    cv2.floodFill(image, None, start_point, fill_color)
    return image


def Rotation(image, angle):
    rot_mat = cv2.getRotationMatrix2D(angle=angle, scale=1., center=(256, 256))
    rotated_circle = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=1)
    return rotated_circle


def combining(inner, external, rotation_steps):
    # rotation
    for step in range(rotation_steps):
        angle = step * rotation_angle
        rotated_inner = Rotation(image=inner, angle=angle)

        #combining
        combination = cv2.addWeighted(external, 0.5, rotated_inner, 0.5, 0)
        gray = cv2.cvtColor(combination, cv2.COLOR_BGR2HSV)[:, :, 2]
        T = cv2.ximgproc.niBlackThreshold(gray, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=81,
                                          k=0.1, binarizationMethod=cv2.ximgproc.BINARIZATION_WOLF)
        grayb = (gray > T).astype("uint8") * 255
        dst = grayb

        # smoothing
        # kernel = np.ones((5, 5), np.float32) / 12
        # dst = cv2.filter2D(grayb, -1, kernel)

        # saving
        new_filename = f'circle_e{external_parts[0]}_i{inner_parts[0]}_s{step}.png'
        output_path = os.path.join(f'{output_folder}/external_{external_parts[0]}', new_filename)
        data = Image.fromarray(dst)
        data.save(output_path)

        # coloring
        output_path_colored = os.path.join(f'{output_folder}_colored/external_{external_parts[0]}', new_filename)
        data_colored = Image.fromarray(coloring(image=dst))
        data_colored.save(output_path_colored)


for external_circle_file in external_circle_files:
    if external_circle_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        external_circle_path = os.path.join(external_arch_folder, external_circle_file)
        # external_circle = cv2.imread(external_circle_path)
        external_circle = read_transparent_png(external_circle_path)

        for inner_circle_file in inner_circle_files:
            if inner_circle_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                inner_circle_path = os.path.join(inner_arch_folder, inner_circle_file)
                # inner_circle = cv2.imread(inner_circle_path)
                inner_circle = read_transparent_png(inner_circle_path)

                # Создание папки с перебором
                inner_parts = inner_circle_file.split('.')
                external_parts = external_circle_file.split('.')
                if f'external_{external_parts[0]}' not in os.listdir(output_folder):
                    os.mkdir(f'{output_folder}/external_{external_parts[0]}')
                if f'external_{external_parts[0]}' not in os.listdir(f'{output_folder}_colored'):
                    os.mkdir(f'{output_folder}_colored/external_{external_parts[0]}')

                # Поворот и сохранение изображений
                combining(inner_circle, external_circle, rotation_steps)

"""Доделать"""
# почистить те, которые не удовлетворяют, потом прогой оставить пересечения по названиям


print('Done!')
end = time.time()
print('Program processed', end-start, 'seconds') # 636 секунд c Pillow без заливки
                                                 # 281 секунд с openCV + заливка + smoothing
                                                 # 108 секунд c openCV без заливки
                                                 # 261 секунд с openCV + заливка с пофикшенным альфа-каналом