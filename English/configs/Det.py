import os
from PIL import Image, ImageDraw
from multiprocessing import Pool


def point_color(a):
    if isinstance(a, int):
        return a
    elif isinstance(a, tuple):
        return sum(a) / len(a)


def stroke_find_black(width, height, x, y, line_y, is_black):
    global to_white
    global connect
    global is_find
    global count
    if connect == 1:
        return
    if y >= min(line_y, height * 0.4):
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
                    stroke_find_black(width, height, x + m, y + n, line_y, is_black)


def stroke_delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color):
    global is_black
    global to_white
    global connect
    global is_find
    global count
    for x, y in top_black:
        is_find = [[0 for j in range(height)] for i in range(width)]
        connect = 0
        count = 0
        stroke_find_black(width, height, x, y, line_y, is_black)
        if connect == 0:
            for m, n in to_white:
                is_black[m][n] = 0
                if n < top_y_end:
                    for i in range(len(top_black)):
                        if top_black[i] == (m, n):
                            top_black.pop(i)
                            break
                if isinstance(editable_pixels[m, n], int):
                    editable_pixels[m, n] = white_color
                elif isinstance(editable_pixels[m, n], tuple):
                    editable_pixels[m, n] = (white_color, white_color, white_color)
        to_white.clear()


def stroke_image(image_path, file_save_folder, filename):
    origin_img = Image.open(image_path)
    img = origin_img.convert("L")
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
            if point_color(editable_pixels[x, y]) < line_black_color:
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
        data = {"img_path": os.path.splitext(filename)[0], "text": "", "scores": -1}
        return data
    line_y = min(line_y, int(height * 0.6))
    stroke_delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color)
    return blank_image(editable_image, file_save_folder, filename)


def blank_delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color):
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
                        if isinstance(editable_pixels[current_line_x, y], int):
                            editable_pixels[current_line_x, y] = white_color
                        elif isinstance(editable_pixels[current_line_x, y], tuple):
                            editable_pixels[current_line_x, y] = (white_color, white_color, white_color)
        last_word_black.clear()
        for x in range(width):
            if point_color(editable_pixels[x, y]) < word_black_color:
                last_word_black.append(x)
    return change_spot


def blank_find_black_line(editable_pixels, width, height):
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
            if point_color(editable_pixels[x, y]) < line_black_color:
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
    return blank_delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color)


def blank_image(img, output_path, filename):
    editable_image = img.copy()
    editable_pixels = editable_image.load()
    width, height = img.size
    black_color = 180
    row_color_threshold = 0.005
    column_color_threshold = 0.03
    is_blank = 1
    blank_distance = 0.035
    for x in range(width):
        is_blank_black_pixel_count = sum(1 for y in range(height) if point_color(editable_pixels[x, y]) < black_color)
        if is_blank_black_pixel_count > height * column_color_threshold:
            is_blank = 0
            break
    if is_blank == 1:
        new_data = {"img_path": os.path.splitext(filename)[0], "text": "", "scores": -1}
        return new_data
    else:
        change_spot = blank_find_black_line(editable_pixels, width, height)
        find = 0
        left_boundary = []
        right_boundary = []
        left_bound = -1
        right_bound = -1
        black_pixel_count2 = 0
        for x in range(width):
            black_pixel_count1 = black_pixel_count2
            black_pixel_count2 = sum(1 for y in range(height) if point_color(editable_pixels[x, y]) < black_color)
            if find == 0 and black_pixel_count1 > height * column_color_threshold and black_pixel_count2 > height * column_color_threshold:
                find = 1
                left_boundary.append(x - 1)
                if right_boundary and left_boundary[-1] - right_boundary[-1] < width * blank_distance:
                    left_boundary.pop(-1)
                    right_boundary.pop(-1)
            if find == 1 and black_pixel_count1 <= height * column_color_threshold and black_pixel_count2 <= height * column_color_threshold:
                find = 0
                right_boundary.append(x)
        if len(left_boundary) == len(right_boundary) + 1:
            right_boundary.append(width - 1)
        if len(left_boundary) == 0:
            new_data = {"img_path": os.path.splitext(filename)[0], "text": "", "scores": -1}
            return new_data
        for (change_x, change_y, color) in change_spot:
            editable_pixels[change_x, change_y] = color
        top_bound = -1
        bottom_bound = -1
        top_boundary = []
        bottom_boundary = []
        for left_bound, right_bound in zip(left_boundary, right_boundary):
            top_add = 1
            for y in range(height):
                top_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if point_color(editable_pixels[x, y]) < black_color)
                if top_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                    top_boundary.append(y)
                    top_add = 0
                    break
            if top_add:
                top_boundary.append(height - 1)
            bottom_add = 1
            for y in range(height - 1, 0, -1):
                bottom_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if point_color(editable_pixels[x, y]) < black_color)
                if bottom_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                    bottom_boundary.append(y)
                    bottom_add = 0
                    break
            if bottom_add:
                bottom_boundary.append(height - 1)
        pop_i = []
        for i in range(len(left_boundary)):
            if right_boundary[i] - left_boundary[i] < 10 or bottom_boundary[i] - top_boundary[i] < 10:
                if (bottom_boundary[i] - top_boundary[i]) / (right_boundary[i] - left_boundary[i]) < 8:
                    pop_i.append(i)
        num = 0
        for i in pop_i:
            right_boundary.pop(i - num)
            left_boundary.pop(i - num)
            top_boundary.pop(i - num)
            bottom_boundary.pop(i - num)
            num = num + 1
        # cropped_img = editable_image.crop((left_bound, top_bound, right_bound, bottom_bound))
        # cropped_img.save(output_path)
        # # 绘制矩形
        # draw = ImageDraw.Draw(editable_image)
        # for left_bound, top_bound, right_bound, bottom_bound in zip(left_boundary, top_boundary, right_boundary, bottom_boundary):
        #     draw.rectangle([left_bound, top_bound, right_bound, bottom_bound], outline='red')
        # editable_image.save(output_path)
        # 多框裁剪
        count = 1
        output_path_without_extension, output_path_extension = os.path.splitext(output_path)
        for left_bound, top_bound, right_bound, bottom_bound in zip(left_boundary, top_boundary, right_boundary, bottom_boundary):
            cropped_img = editable_image.crop((left_bound, top_bound, right_bound, bottom_bound))
            save_path = output_path_without_extension + '_' + str(count).zfill(2) + output_path_extension
            cropped_img.save(save_path)
            count += 1
        return []


def process_image(args):
    folderIn_path, folder_det, filename = args
    image_path = os.path.join(folderIn_path, filename)
    file_save_folder = os.path.join(folder_det, filename)
    data = stroke_image(image_path, file_save_folder, filename)
    return data


def det(folderIn_path, folder_det):
    data_list = []
    args = [(folderIn_path, folder_det, filename) for filename in os.listdir(folderIn_path)]
    with Pool() as pool:
        datas = pool.map(process_image, args)
    for data in datas:
        if data != []:
            data_list.append(data)
    return data_list
