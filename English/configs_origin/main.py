import argparse
from Strokes import strokes
from Blank import blank
from Recog import recog
from tqdm import tqdm
import datetime
import os
import shutil


def count_images_in_folder(folder_path):
    image_count = 0
    for filename in os.listdir(folder_path):
        fileInpath = os.path.join(folder_path, filename)
        if os.path.isdir(fileInpath):
            image_count += count_images_in_folder(fileInpath)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            image_count += 1
    return image_count


def process_images_in_folder(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar, model):
    if not os.path.exists(folder_stroke):
        os.makedirs(folder_stroke)
    if not os.path.exists(folder_blank):
        os.makedirs(folder_blank)
    if not os.path.exists(folder_result):
        os.makedirs(folder_result)
    for filename in os.listdir(folderIn_path):
        new_fileInpath = os.path.join(folderIn_path, filename)
        if os.path.isdir(new_fileInpath):
            new_folder_stroke = os.path.join(folder_stroke, filename)
            new_folder_blank = os.path.join(folder_blank, filename)
            new_folder_result = os.path.join(folder_result, filename)
            process_images_in_folder(new_fileInpath, new_folder_stroke, new_folder_blank, new_folder_result, progress_bar, model)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            process(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar, model)
            break
    shutil.rmtree(folder_stroke)
    shutil.rmtree(folder_blank)


def process(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar, model):
    current_time1 = datetime.datetime.now()
    data_list = strokes(folderIn_path, folder_stroke)
    data_list = blank(folder_stroke, folder_blank, data_list, progress_bar)

    current_time3 = datetime.datetime.now()
    print("一二步总时间")
    print(current_time3 - current_time1)
    recog(folder_blank, folder_result, data_list, model)

    current_time4 = datetime.datetime.now()
    print("第三步总时间")
    print(current_time4 - current_time3)


current_time1 = datetime.datetime.now()
parser = argparse.ArgumentParser(description='Recognization')
parser.add_argument('input_folder', type=str, help='The path to the image')
parser.add_argument('output_folder', type=str, help='The path to the result')
parser.add_argument('model_name', type=str, help='fast/accurate')
args = parser.parse_args()

progress_bar = tqdm(total=count_images_in_folder(args.input_folder), desc='Processing')
Romaning_path = os.path.join(args.output_folder, 'Romaning')
if not os.path.exists(Romaning_path):
    os.makedirs(Romaning_path)
stroke_path = os.path.join(Romaning_path, 'stroke')
blank_path = os.path.join(Romaning_path, 'blank')
result_path = os.path.join(args.output_folder, 'result')
process_images_in_folder(args.input_folder, stroke_path, blank_path, result_path, progress_bar, args.model_name)
shutil.rmtree(Romaning_path)
progress_bar.close()
current_time2 = datetime.datetime.now()
print("总时间")
print(current_time2 - current_time1)
