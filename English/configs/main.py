import argparse
from Det import det
from Recog import recog
import datetime
import os
import shutil


def process_images_in_folder(folderIn_path, folder_det, folder_result, model):
    if not os.path.exists(folder_det):
        os.makedirs(folder_det)
    if not os.path.exists(folder_result):
        os.makedirs(folder_result)
    for filename in os.listdir(folderIn_path):
        new_fileInpath = os.path.join(folderIn_path, filename)
        if os.path.isdir(new_fileInpath):
            new_folder_det = os.path.join(folder_det, filename)
            new_folder_result = os.path.join(folder_result, filename)
            process_images_in_folder(new_fileInpath, new_folder_det, new_folder_result, model)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            process(folderIn_path, folder_det, folder_result, model)
            break
    shutil.rmtree(folder_det)


def process(folderIn_path, folder_det, folder_result, model):
    data_list = det(folderIn_path, folder_det)
    recog(folder_det, folder_result, data_list, model)


current_time1 = datetime.datetime.now()
parser = argparse.ArgumentParser(description='Recognization')
parser.add_argument('input_folder', type=str, help='The path to the image')
parser.add_argument('output_folder', type=str, help='The path to the result')
parser.add_argument('model_name', type=str, help='fast/accurate')
args = parser.parse_args()

Romaning_path = os.path.join(args.output_folder, 'Romaning')
if not os.path.exists(Romaning_path):
    os.makedirs(Romaning_path)
det_path = os.path.join(Romaning_path, 'det')
result_path = os.path.join(args.output_folder, 'result')
process_images_in_folder(args.input_folder, det_path, result_path, args.model_name)
shutil.rmtree(Romaning_path)
current_time2 = datetime.datetime.now()
print("整体总时间")
print(current_time2 - current_time1)
