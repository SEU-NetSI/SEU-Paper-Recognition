from PIL import Image, ImageDraw
import json
import shutil
import cv2
import numpy as np
import os

num = 1
def cut_json(json_file, image_file, type_num, range): # json文件，图片，region类型
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    cropped_images = []

    for region in data['regions']:
        if region.get('regionType') == type_num:
            x, y, w, h = (
                region.get('regionLeft'),
                region.get('regionTop'),
                region.get('regionWidth'),
                region.get('regionHeight')
            )
            image = Image.open(image_file)
            # 适当扩大范围
            cropped_image = image.crop((x - range, y - range, x + w + range, y + h + range))
            cropped_images.append(cropped_image)

    return cropped_images
def cut_contour(cropped_images, edge = 2, width = 1493, height = 5): # json切完图片列表，边缘阈值，得分条长度，延长高度
    cropped_results = []

    for pil_image in cropped_images:
        # 将 PIL 图像转换为 NumPy 数组
        original_image = np.array(pil_image)
        original_image = original_image[:, :, ::-1]
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 定义边缘排除阈值
        edge_threshold = edge
        min_x, min_y, max_w, max_h = float('inf'), float('inf'), 0, 0

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if x > edge_threshold and y > edge_threshold and x + w < original_image.shape[1] - edge_threshold and y + h < original_image.shape[0] - edge_threshold:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_w = max(max_w, x + w)
                max_h = max(max_h, y + h)

        min_x, min_y, max_w, max_h = int(min_x), int(min_y), int(max_w), int(max_h)

        if max_w - min_x >= width:
            cropped_image = original_image[min_y - height:max_h + height, min_x:max_w]
        else:
            left_distance = min_x
            right_distance = original_image.shape[1] - max_w
            if left_distance < right_distance:
                cropped_image = original_image[min_y - height:max_h + height, min_x:min_x + width]
            else:
                cropped_image = original_image[min_y - height:max_h + height, max_w - width:max_w]

        cropped_results.append(cropped_image)

    return cropped_results
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

def pic_handle(image, save_path = None):
    # 切割图像
    pic_set = split_image(image, 22)

    color_list = []

    for pic in pic_set:
        # p=remove_black_border(pic)
        i = detect_red_pixels(pic)
        color_list.append(i)

    # 检查列表中的值是否全部为零
    if all(num == 0 for num in color_list):
        print(f"第_{num}_题图中无批改痕迹")
    else:
        # 获取拥有最多红色像素点的子图
        max_index = get_max_index(color_list)

        print(f"第_{num}_题红色点最多的子图为：", max_index)
        if save_path != None:
            draw_red_circle(image, max_index, save_path)

# 使用示例
cropped_images_list = cut_json('test3.json', 'test10.jpg', 101, range =10)
processed_images = cut_contour(cropped_images_list, edge= 2)
for image in processed_images:
    pic_handle(image)
    num += 1