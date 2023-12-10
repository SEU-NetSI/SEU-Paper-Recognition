import cv2
import numpy as np
import os
import time


def split_image(image, num_splits):
    """
    将图像从左到右均匀切割为指定数量的子图，并保存为子图列表
    """
    height, width, _ = image.shape
    split_width = width // num_splits
    splits = []

    for i in range(num_splits):
        left = i * split_width
        right = (i + 1) * split_width
        split = image[:, left:right, :]
        splits.append(split)

    return splits


def remove_black_border(image):
    """
    去除图像中的黑色边框
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped_image = image[y:y + h, x:x + w]

    return cropped_image


def detect_red_pixels(image):
    """
    检测图像中的红色像素点
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 200])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 50, 200])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.bitwise_or(mask1, mask2)
    red_pixels = np.where(mask == 255)
    num_red = len(red_pixels[0])
    return num_red


def get_max_index(lst):
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index


def draw_red_circle(image, x, save_path):
    # 获取图片的宽度和高度
    image_height, image_width, _ = image.shape

    # 计算每份的宽度
    num_sub_images = 22
    sub_image_width = image_width // num_sub_images

    # 计算圆点的位置
    circle_radius = 10
    circle_color = (255, 0, 0)  # 蓝色
    circle_thickness = -1  # -1表示实心圆
    sub_image_x = x * sub_image_width
    circle_center = (sub_image_x + sub_image_width // 2, image_height // 2)

    # 在图片上绘制圆点
    cv2.circle(image, circle_center, circle_radius, circle_color, circle_thickness)

    # 保存图像
    cv2.imwrite(save_path, image)


def pic_handle(image_path, save_path):
    # 记录开始时间
    start_time = time.time()

    # 读取图像
    image = cv2.imread(image_path)

    # 切割图像
    pic_set = split_image(image, 22)

    color_list = []

    for pic in pic_set:
        # p=remove_black_border(pic)
        i = detect_red_pixels(pic)
        color_list.append(i)

    # 检查列表中的值是否全部为零
    if all(num == 0 for num in color_list):
        print("图中无批改痕迹")
    else:
        # 获取拥有最多红色像素点的子图
        max_index = get_max_index(color_list)

        print("红色点最多的子图为：", max_index, "绘制标志点并保存")

        draw_red_circle(image, max_index, save_path)

    # 记录结束时间
    end_time = time.time()
    # 计算运行时间
    run_time = end_time - start_time
    print("程序运行时间：", run_time, "秒")

pic_handle("cut_102.jpg", 'cut_102_reasult.jpg')