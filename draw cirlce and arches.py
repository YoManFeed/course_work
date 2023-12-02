from PIL import Image, ImageDraw
import math


def draw_circle(image, x, y, radius, color="black"):
    """
    Рисует окружность на изображении.

    Параметры:
    - image: объект изображения (Image)
    - x, y: координаты центра окружности
    - radius: радиус окружности
    - color: цвет контура окружности (по умолчанию "black")
    """
    draw = ImageDraw.Draw(image)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=thickness)


def draw_horizontal_line(x, y, length, angle, color="black", thickness=3):
    """
    Рисует горизонтальную прямую на изображении.

    Параметры:
    - image: объект изображения (Image)
    - x, y: координаты начала прямой
    - length: длина прямой
    - color: цвет прямой (по умолчанию "black")
    - thickness: толщина прямой (по умолчанию 1)
    """
    draw = ImageDraw.Draw(image)

    # Вычисляем координаты конечной точки
    x2 = x + int(length * math.cos(math.radians(angle)))
    y2 = y + int(length * math.sin(math.radians(angle)))

    draw.line((x, y, x2, y2), fill=color, width=thickness)
    # draw = ImageDraw.Draw(image)
    # draw.line((x, y, x + length, y), fill=color, width=thickness)


def draw_small_circle_up(x_dot, y_dot, r, alpha):
    phi = math.atan((r/(128-r)))
    x = x_dot
    y = y_dot
    start_angle = 180 + math.degrees(alpha)
    end_angle = 270 + math.degrees(alpha)

    draw = ImageDraw.Draw(image)
    draw.arc(
        (x - r, y - r, x + r, y + r),
        start=start_angle,
        end=end_angle,
        fill='brown',
        width=3,
    )


def draw_small_circle_bottom(x_dot, y_dot, r):
    draw = ImageDraw.Draw(image)
    draw.arc(
        (x_dot - r, y_dot - 2 * r, x_dot+r, y_dot),
        start=90,
        end=180,
        fill='black',
        width=3,
    )


def generate_circle_points(center, radius, num_points):
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        x = center[0] + int(radius * math.cos(angle))
        y = center[1] + int(radius * math.sin(angle))
        points.append((x, y))
    return points


def connect_circles(x, y, alpha, r, R):
    phi = math.atan((r / (R + r)))
    start_angle = 180 + math.degrees(phi)
    end_angle = 180 + math.degrees(alpha) - math.degrees(phi)
    draw = ImageDraw.Draw(image)
    draw.arc(
        (x-R, y-R, x+R, y+R),
        start=start_angle,
        end=end_angle,
        fill='red',
        width=3,
    )


if __name__ == '__main__':
    image_size = (512, 512)
    image = Image.new("RGB", image_size, "white")
    center = (image_size[0] // 2, image_size[1] // 2)
    radius = 128
    thickness = 3

    draw_circle(image, 256, 256, 128, color='red')
    draw_circle(image, 128, 238, 18, color='blue')
    draw_horizontal_line(256, 256, 512, -150)
    draw_horizontal_line(256, 256, 512, -180)

    for i in range(6):
        small_radius = 18+18*i
        draw_small_circle_bottom(128, 256, small_radius)

    num_points = 12  # Измените на желаемое количество точек

    points_on_circle = generate_circle_points(center, radius, num_points)

    points_on_circle = points_on_circle[len(points_on_circle) // 2:] + points_on_circle[:len(points_on_circle) // 2]

    R = 128
    r = 18
    for i, point in enumerate(points_on_circle):
        if i % 2 == 1:
            r = 18 + 18 * (i // 2)
            angle = (i / num_points) * 2 * math.pi
            draw_small_circle_up(point[0] - r * math.sin(angle), point[1] + r * math.cos(angle), r, alpha=angle)
            R_connect = (math.sqrt(R**2 + (r - (r**2/(R-r)))**2)) * (1 + r/R)
            # connect_circles(256, 256, angle, r, R_connect)
            # connect_circles(point[0] - r * math.sin(angle), point[1] + r * math.cos(angle), angle, r, r+1)
            connect_circles(256, 256, angle, r, R_connect)

    image.show()
