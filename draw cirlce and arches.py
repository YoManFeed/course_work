import cv2
from PIL import Image, ImageDraw
import math
from settings import *
from working_with_images import show_me


def draw_circle(x, y, radius, color="black"):
    draw = ImageDraw.Draw(image)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=thickness)


def draw_horizontal_line(x, y, length, angle, color="red", thickness=3):
    draw = ImageDraw.Draw(image)
    x2 = x + int(length * math.cos(math.radians(angle)))
    y2 = y + int(length * math.sin(math.radians(angle)))

    draw.line((x, y, x2, y2), fill=color, width=thickness)


def draw_small_circle_up(x_dot, y_dot, r, alpha):
    x = x_dot
    y = y_dot
    start_angle = 180 + math.degrees(alpha)
    end_angle = 270 + math.degrees(alpha)

    draw = ImageDraw.Draw(image)
    draw.arc(
        (x - r, y - r, x + r, y + r),
        start=start_angle,
        end=end_angle,
        fill='black',
        width=thickness,
    )


def draw_small_circle_bottom(x_dot, y_dot, r):
    draw = ImageDraw.Draw(image)
    draw.arc(
        (x_dot - r, y_dot - 2 * r, x_dot+r, y_dot),
        start=90,
        end=180,
        fill='black',
        width=thickness,
    )
    return draw


def generate_circle_points(center, radius, num_points):
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        x = center[0] + int(radius * math.cos(angle))
        y = center[1] + int(radius * math.sin(angle))
        points.append((x, y))
    return points


def connect_circles(x, y, alpha, r, R):
    R_c = (math.sqrt(R ** 2 + (r * R / (R + r)) ** 2) + math.sqrt(r ** 2 + (r ** 2 / (R + r)) ** 2))
    phi = math.atan((r / (R + r)))
    start_angle = 180 + math.degrees(phi)
    end_angle = 180 + math.degrees(alpha) - math.degrees(phi)
    draw = ImageDraw.Draw(image)
    draw.arc(
        (x-R_c, y-R_c, x+R_c, y+R_c),
        start=start_angle,
        end=end_angle,
        fill='black',
        width=thickness,
    )


if __name__ == '__main__':
    image_size = (512, 512)
    center = (image_size[0] // 2, image_size[1] // 2)
    thickness = 3

    deg = 6
    num_points = 2 * deg
    R = image_size[0] // 4
    D = 2*R
    r = R // (deg+2)

    # image = Image.new("RGB", image_size, "white")
    # draw = ImageDraw.Draw(image)

    points_on_circle = generate_circle_points(center, R, num_points)
    points_on_circle = points_on_circle[num_points // 2:] + points_on_circle[:num_points // 2]

    for i, point in enumerate(points_on_circle):
        if i % 2 == 1:
            angle = (i / num_points) * 2 * math.pi
            r_upd = r + r * (i // 2)

            image = Image.new("RGB", image_size, "white")
            draw_circle(D, D, R, color='black')

            draw_small_circle_bottom(R, D, r_upd)
            draw_small_circle_up(point[0] - r_upd * math.sin(angle), point[1] + r_upd * math.cos(angle), r_upd, alpha=angle)
            connect_circles(D, D, angle, r_upd, R)

            # file_path = os.path.join()
            # image.save(file_path)

    x1=points_on_circle[0][0]
    y1=points_on_circle[0][1]

    x2=points_on_circle[1][0]
    y2=points_on_circle[1][1]

    draw_horizontal_line(x1,y1,5,0)
    draw_horizontal_line(x2,y2,5,0)

    image_np = np.array(image)
    image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    ro = 33
    # ro = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    print(ro)
    axes = (ro, int(math.sqrt(5)*ro/4))
    angle = -75  # Угол поворота в градусах
    color = (0, 0, 0)
    thickness = 2

    cv2.ellipse(image_cv2, center, axes, angle, 0, 180, color, thickness)

    show_me(image_cv2)
