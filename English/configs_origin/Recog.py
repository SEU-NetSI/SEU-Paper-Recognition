from mmocr.apis import TextRecInferencer
import os
import json
import shutil
import datetime


def read_json_files(folder_path, data_list):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                text = data['text']
                scores = data['scores']
                new_data = {
                    "img_path": os.path.splitext(filename)[0],
                    "text": text,
                    "scores": scores
                }
                data_list.append(new_data)
    result_json_path = os.path.dirname(folder_path) + ".json"
    with open(result_json_path, 'w') as file:
        json.dump(data_list, file)
    shutil.rmtree(os.path.dirname(folder_path))


def recog(folder_blank, folder_result, data_list, model):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.dirname(current_dir)
    model_name = "model_" + model
    model_path = os.path.join(parent_dir, model_name, "config.py")
    weight_path = os.path.join(parent_dir, model_name, "weight.pth")
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

    # current_time1 = datetime.datetime.now()

    inferencer = TextRecInferencer(model=model_path, weights=weight_path)
    inferencer(folder_blank, out_dir=folder_result, save_pred=True)

    # current_time2 = datetime.datetime.now()
    # print("第三步")
    # print(current_time2 - current_time1)

    read_json_files(os.path.join(folder_result, 'preds'), data_list)

    # current_time3 = datetime.datetime.now()
    # print("第三步")
    # print(current_time3 - current_time2)

