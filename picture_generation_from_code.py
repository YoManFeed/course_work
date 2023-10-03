import time

import numpy as np
import os
import cv2


def show_me(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def read_transparent_png(img_path):
    image_4channel = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:, :, 3]
    rgb_channels = image_4channel[:, :, :3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:, :, np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor, alpha_factor, alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white

    return final_image.astype(np.uint8)


def remove_background(image_path):
    """Sometimes artefacts occurs on the image. Try another method to read the image:"""
    # image = cv2.imread(image_path)  # with white background
    image = read_transparent_png(image_path)  # with transparent background

    # makes mask that shows if pixel falls into a specific range in BGR color space
    lower_color = np.array([150, 150, 150], dtype=np.uint8)
    upper_color = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(image, lower_color, upper_color)

    # creates alpha channel where all pixels in range are transparent
    alpha_channel = np.where(mask > 0, 0, 255).astype(np.uint8)
    image_with_transparency = cv2.merge((image[:, :, :3], alpha_channel))

    # coloring all pixels that are not transparent
    black_mask = (alpha_channel == 255)
    image_with_transparency[black_mask] = [0, 0, 0, 255]

    return image_with_transparency


def draw_circle(image):
    height, width, _ = image.shape
    center = (width // 2, height // 2)
    circle_color = (0, 0, 0)
    radius = 128
    cv2.circle(image, center, radius, circle_color, thickness=2)
    return image


def combine(img1, img2):
    alpha_1 = img1[:, :, 3]
    alpha_2 = img2[:, :, 3]

    rgb_1 = img1[:, :, :3]
    rgb_2 = img2[:, :, :3]

    merged_alpha = cv2.bitwise_or(alpha_1, alpha_2)
    merged_bw = cv2.bitwise_and(rgb_1, rgb_2)

    result = np.zeros_like(img1)
    result[:, :, :3] = merged_bw
    result[:, :, 3] = merged_alpha

    return result


def rotation(image, angle):
    rot_mat = cv2.getRotationMatrix2D(angle=angle, scale=1., center=(256, 256))
    rotated_circle = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=1)
    return rotated_circle


if __name__ == '__main__':
    current_dir = os.path.join('/Users/popit/Desktop')
    image_path_1 = os.path.join(current_dir, 'circle.png')
    img_paths = [''] * 7
    images = [0] * 7

    img_paths[0] = os.path.join(current_dir, 'circle.png')
    images[0] = remove_background(img_paths[0])
    for i in range(1, 7):
        img_paths[i] = os.path.join(current_dir, f'arch_{i}.png')
        print(img_paths[i])
        images[i] = remove_background(img_paths[i])

    rotation_steps = 12
    rotation_angle = 360 / rotation_steps
    code = [6, 5, 1, 0, 3, 1, 0, 1, 0, 0, 0, 0]
    temp = images[0]

    for i in range(rotation_steps):
        angle = i * rotation_angle
        arch_index = code[i]
        print(code[i])
        show_me(temp)
        if arch_index != 0:
            rotated = rotation(images[arch_index], angle)
            temp = combine(temp, rotated)

    show_me(temp)
    output_path = os.path.join(current_dir, 'output.png')
    cv2.imwrite(output_path, temp)