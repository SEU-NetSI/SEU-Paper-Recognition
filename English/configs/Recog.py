from mmocr.apis import TextRecInferencer
import os
import json
import shutil


def read_json_files(folder_path, data_list):
    processed_file = []
    for filename in os.listdir(folder_path):
        truename = filename[:-8]
        if filename.endswith('.json') and truename not in processed_file:
            processed_file.append(truename)
            count = 1
            text = ''
            scores = ''
            current_name = truename + '_' + str(count).zfill(2) + '.json'
            while current_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, current_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    text += data['text'] + ' '
                    scores += str(data['scores']) + '+'
                count += 1
                current_name = truename + '_' + str(count).zfill(2) + '.json'
            new_data = {
                "img_path": truename,
                "text": text[:-1],
                "scores": scores[:-1]
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
    inferencer = TextRecInferencer(model=model_path, weights=weight_path)
    inferencer(folder_blank, out_dir=folder_result, save_pred=True, batch_size=1024, progress_bar=False)
    read_json_files(os.path.join(folder_result, 'preds'), data_list)
