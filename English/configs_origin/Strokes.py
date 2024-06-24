import os
from PIL import Image


def find_black(width, height, x, y, line_y, is_black):
    global to_white
    global connect
    global is_find
    global count
    if connect == 1:
        return
    if y >= line_y:
        connect = 1
        return
    if count > 900:
        connect = 1
        return
    for m in range(-1, 2):
        for n in range(-1, 2):
            if 0 <= x + m < width and 0 <= y + n < height:
                if is_find[x + m][y + n] == 0 and is_black[x + m][y + n] == 1:
                    is_find[x + m][y + n] = 1
                    to_white.append((x + m, y + n))
                    count = count + 1
                    find_black(width, height, x + m, y + n, line_y, is_black)


def delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color):
    global is_black
    global to_white
    global connect
    global is_find
    global count
    for x, y in top_black:
        is_find = [[0 for j in range(height)] for i in range(width)]
        connect = 0
        count = 0
        find_black(width, height, x, y, line_y, is_black)
        if connect == 0:
            for m, n in to_white:
                is_black[m][n] = 0
                if n < top_y_end:
                    for i in range(len(top_black)):
                        if top_black[i] == (m, n):
                            top_black.pop(i)
                            break
                editable_pixels[m, n] = white_color
        to_white.clear()


def crop_image(image_path, file_save_folder, filename, data_list):
    img = Image.open(image_path)
    editable_image = img.copy()
    editable_pixels = editable_image.load()
    width, height = img.size
    line_black_color = 240
    row_color_threshold = 0.4
    white_color = 255
    top_y_end = 2
    bottom_y_end = 1
    current_line_black = []
    top_black = []
    bottom_black = []
    global is_black
    is_black = [[0 for j in range(height)] for i in range(width)]
    global to_white
    to_white = []
    line_to_white = []
    find_top_line_y = 0
    line_y = -1
    for y in range(height):
        current_line_black.clear()
        find_line = 0
        for x in range(width):
            if editable_pixels[x, y] < line_black_color:
                current_line_black.append(x)
                is_black[x][y] = 1
                if y < top_y_end:
                    top_black.append((x, y))
                if y > height - 1 - bottom_y_end:
                    bottom_black.append((x, y))
        black_pixel_count = len(current_line_black)
        if black_pixel_count > width * row_color_threshold:
            find_line = 1
        if find_line == 1 and y > height * 0.5 and find_top_line_y == 0:
            line_y = y
            find_top_line_y = 1
        if find_line == 1 and y > height * 0.5:
            for i in range(-1, 2):
                if 0 <= y + i < height:
                    no_add = 0
                    for delete_line in line_to_white:
                        if y + i == delete_line:
                            no_add = 1
                            break
                    if no_add == 0:
                        line_to_white.append(y + i)
    if line_y == -1:
        data = {
            "img_path": os.path.splitext(filename)[0],
            "text": "",
            "scores": -1
        }
        data_list.append(data)
        return data_list
    line_y = min(line_y, int(height * 0.6))
    delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color)
    editable_image.save(file_save_folder)
    return data_list


def strokes(folderIn_path, folder_stroke):
    data_list = []
    for filename in os.listdir(folderIn_path):
        image_path = os.path.join(folderIn_path, filename)
        file_save_folder = os.path.join(folder_stroke, filename)
        data_list = crop_image(image_path, file_save_folder, filename, data_list)
    return data_list
