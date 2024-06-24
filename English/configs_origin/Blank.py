import os
from PIL import Image


def delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color):
    last_word_black = []
    change_spot = []
    for y in range(height):
        for delete_y in line_to_white:
            if y == delete_y:
                for current_line_x in range(width):
                    change_spot.append((current_line_x, y, editable_pixels[current_line_x, y]))
                    find_black = 0
                    for last_word_x in last_word_black:
                        if abs(current_line_x - last_word_x) <= 0:
                            find_black = 1
                            break
                    if find_black == 0:
                        editable_pixels[current_line_x, y] = white_color
        last_word_black.clear()
        for x in range(width):
            if editable_pixels[x, y] < word_black_color:
                last_word_black.append(x)
    return change_spot


def find_black_line(editable_pixels, width, height):
    line_black_color = 220
    word_black_color = 130
    row_color_threshold = 0.4
    white_color = 255
    current_line_black = []
    line_to_white = []
    for y in range(height):
        current_line_black.clear()
        find_line = 0
        for x in range(width):
            if editable_pixels[x, y] < line_black_color:
                current_line_black.append(x)
        black_pixel_count = len(current_line_black)
        if black_pixel_count > width * row_color_threshold:
            find_line = 1
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
    return delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color)


def crop_image(image_path, output_path, filename, data_list):
    img = Image.open(image_path)
    editable_image = img.copy()
    editable_pixels = editable_image.load()
    width, height = img.size
    black_color = 180
    row_color_threshold = 0.005
    column_color_threshold = 0.03
    is_blank = 1
    for x in range(width):
        is_blank_black_pixel_count = sum(1 for y in range(height) if editable_pixels[x, y] < black_color)
        if is_blank_black_pixel_count > height * column_color_threshold:
            is_blank = 0
            break
    if is_blank == 1:
        new_data = {
            "img_path": os.path.splitext(filename),
            "text": "",
            "scores": -1
        }
        data_list.append(new_data)
        return data_list
    else:
        change_spot = find_black_line(editable_pixels, width, height)
        find = 0
        left_boundary = []
        right_boundary = []
        left_bound = -1
        right_bound = -1
        black_pixel_count2 = 0
        for x in range(width):
            black_pixel_count1 = black_pixel_count2
            black_pixel_count2 = sum(1 for y in range(height) if editable_pixels[x, y] < black_color)
            if find == 0 and black_pixel_count1 > height * column_color_threshold and black_pixel_count2 > height * column_color_threshold:
                find = 1
                left_boundary.append(x - 1)
            if find == 1 and black_pixel_count1 <= height * column_color_threshold and black_pixel_count2 <= height * column_color_threshold:
                find = 0
                right_boundary.append(x)
        if len(left_boundary) == len(right_boundary) + 1:
            right_boundary.append(width - 1)
        if len(left_boundary) == 0:
            new_data = {
                "img_path": os.path.splitext(filename)[0],
                "text": "",
                "scores": -1
            }
            data_list.append(new_data)
            return data_list
        else:
            left_bound = left_boundary[0]
            right_bound = right_boundary[-1]
        for (change_x, change_y, color) in change_spot:
            editable_pixels[change_x, change_y] = color
        top_bound = -1
        bottom_bound = -1
        for y in range(height):
            top_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if editable_pixels[x, y] < black_color)
            if top_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                top_bound = y
                break
        for y in range(height - 1, 0, -1):
            bottom_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if editable_pixels[x, y] < black_color)
            if bottom_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                bottom_bound = y
                break
        if top_bound == -1 or bottom_bound == -1:
            print(image_path)
        cropped_img = editable_image.crop((left_bound, top_bound, right_bound, bottom_bound))
        cropped_img.save(output_path)
        return data_list


def blank(folder_stroke, folder_blank, data_list, progress_bar):
    for filename in os.listdir(folder_stroke):
        image_path = os.path.join(folder_stroke, filename)
        file_save_folder = os.path.join(folder_blank, filename)
        data_list = crop_image(image_path, file_save_folder, filename, data_list)
        progress_bar.update(1)
    return data_list
