"""
This file will fetch train and test csv and then convert the data into JSON.
"""
__author__ = "Hartaran Singh"
import json
import os
import csv
from tqdm import tqdm

def create_dataset(input_file_path, output_file_path):
    """
    This Function Creates JSON Flat files  for input csv and Create mutliple jsons of size at max=40000.
    :param input_file_path: CSV file path
    :param output_file_path: output file path
    :return: None
    """
    col_index_map = {'user_id': 0, 'session_id': 1, 'timestamp': 2, 'step': 3, 'action_type': 4, 'reference': 5,
                     'platform': 6, 'city': 7, 'device': 8,
                     'current_filters': 9, 'impressions': 10, 'prices': 11}
    flat_dict = dict()
    with open(input_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        header = next(reader)
        col_names = [col_name for col_name in col_index_map.keys()]
        col_names.pop(0)
        index = 0
        for row in tqdm(reader):
            if len(flat_dict) > 40000:
                index += 1
                with open(output_file_path + "_" + str(index) + ".json", "w") as file:
                    json.dump(flat_dict, file)
                print(" JSON : ", index)
                flat_dict = dict()
            col_values = [row[col_index_map[c_n]] for c_n in col_names]
            dict_for_each_row = dict(zip(col_names, col_values))
            to_list = dict_for_each_row['impressions']
            dict_for_each_row['impressions'] = to_list.split('|')
            to_list = dict_for_each_row['prices']
            dict_for_each_row['prices'] = to_list.split('|')
            user_id = row[col_index_map['user_id']]
            if user_id in flat_dict:
                flat_dict[user_id].append(dict_for_each_row)
            else:
                flat_dict[user_id] = [dict_for_each_row]

    print("Output is Saved")


if __name__ == "__main__":
    cwd = os.getcwd()
    # TODO: Change Train and Test path as per your system before running.

    test_set_path = "/../../../trivagoRecSysChallengeData2019_v2/test.csv"
    test_set_path = cwd + test_set_path
    #
    train_set_path = "/../../../trivagoRecSysChallengeData2019_v2/train.csv"
    train_set_path = cwd + train_set_path

    print("Creating Dataset For Test Data")
    output_file_path = cwd + "/../Generated_Dataset/Testset/"
    create_dataset(test_set_path, output_file_path + "testset")

    print("Creating Dataset For Train Data")
    output_file_path = cwd + "/../Generated_Dataset/Trainset/"
    create_dataset(train_set_path, output_file_path + "trainset")
