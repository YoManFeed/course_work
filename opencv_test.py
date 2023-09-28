from PIL import Image
import numpy as np
import os
import cv2


def read_transparent_png(img_path):
    image_4channel = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:,:,3]
    rgb_channels = image_4channel[:,:,:3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor, alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white
    return final_image.astype(np.uint8)


current_dir = os.path.join('/Users/popit/Desktop')
arch_1_path = os.path.join(current_dir, 'arch_1.png')
arch_3_path = os.path.join(current_dir, 'arch_3.png')
arch_5_path = os.path.join(current_dir, 'arch_5.png')
arch_6_path = os.path.join(current_dir, 'arch_6.png')
circle_path = os.path.join(current_dir, 'circle_sample.png')
# arch_1 = read_transparent_png(arch_1_path)
# arch_3 = read_transparent_png(arch_3_path)
# arch_5 = read_transparent_png(arch_5_path)
# arch_6 = read_transparent_png(arch_6_path)
# circle = read_transparent_png(circle_path)
arch_1 = cv2.imread(arch_1_path, cv2.IMREAD_UNCHANGED)
arch_3 = cv2.imread(arch_3_path, cv2.IMREAD_UNCHANGED)
arch_5 = cv2.imread(arch_5_path, cv2.IMREAD_UNCHANGED)
arch_6 = cv2.imread(arch_6_path, cv2.IMREAD_UNCHANGED)
circle = cv2.imread(circle_path, cv2.IMREAD_UNCHANGED)

# print(circle)

def show_me(image):
    try:
        cv2.imshow('image', image)
        cv2.resizeWindow('image', 800, 800)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        pass
# show_me(circle)

def Rotation(image, angle):
    rot_mat = cv2.getRotationMatrix2D(angle=angle, scale=1., center=(256, 256))
    rotated_circle = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=1)
    return rotated_circle


def refactoring_the_code(code: str) -> list:
    filling = [-1]*12
    ones = []
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
def making_archs(refactored_code: list) -> list:
    copied = refactored_code.copy()[::-1]
    sequence = []
    left_index = -1
    for elem in refactored_code:
        left_index += 1
        right_index = len(refactored_code) - copied.index(elem)
        difference = right_index - left_index
        sequence.append(int(difference/2))
    return sequence


def combining(inner, external):
    # print('inner shape:', inner.shape, 'external shape:', external.shape)
    inner_alpha = inner[:, :, 3]
    external_alpha = external[:, :, 3]
    alpha_channel = inner_alpha | external_alpha

    combination = cv2.addWeighted(external, 1, inner, 1, 1)
    # print(combination.shape)
    # alpha_channel = combination[:, :, 3]
    # print('alpha_channel shape', alpha_channel.shape)
    gray = cv2.cvtColor(combination, cv2.COLOR_BGR2HSV)[:, :, 2]
    T = cv2.ximgproc.niBlackThreshold(gray, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=81,
                                      k=0.1, binarizationMethod=cv2.ximgproc.BINARIZATION_WOLF)
    grayb = (gray > T).astype("uint8") * 255
    dst = cv2.merge((grayb, grayb, grayb, alpha_channel))
    # print(dst.shape)
    return dst


rotation_steps = 12
rotation_angle = 360/rotation_steps
code = '111011010000'

Null_image = np.full((512, 512, 4), (255, 255, 255, 0), dtype=np.uint8)
archs = [Null_image, arch_1, Null_image, arch_3, Null_image, arch_5, arch_6]

print(refactoring_the_code(code))
print(making_archs([11, 10, 3, 3, 9, 6, 6, 8, 8, 9, 10, 11]))
archs_length = making_archs([11, 10, 3, 3, 9, 6, 6, 8, 8, 9, 10, 11])


def drawing_archs(arcs_length: list):
    global rotation_steps
    image = circle
    for i in range(len(arcs_length)):
        print(arcs_length[i])
        if arcs_length[i] == 0:
            pass
        else:
            external = archs[archs_length[i]]
            image = combining(image, external)
            # show_me(image)
            print('image shape:', image.shape)
    return image


result = drawing_archs([6, 5, 1, 0, 3, 1, 0, 1, 0, 0, 0, 0])
output_path = os.path.join(current_dir, 'output.png')



