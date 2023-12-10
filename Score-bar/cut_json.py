from PIL import Image, ImageDraw
import json
import shutil
import cv2
import numpy as np
import os
num = 0
def cut_json(json_file, image_file, type_num): # json文件，图片，region类型
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
            cropped_image = image.crop((x - 8, y - 8, x + w + 8, y + h + 8))
            cropped_images.append(cropped_image)

    return cropped_images

cropped_images_list = cut_json('test3.json', 'test_b.jpg', 101)
