import os
import requests
import sys
import pickle
import utils
import constants
import split_file
import parse_labels
S = requests.Session()


def restart_elastic_index():
    utils.report_process("restart_elastic_index started")
    es = utils.elastic_connect()
    for i in es.indices.get('*'):
        if i == constants.ELASTIC_INDEX:
            es.indices.delete(index=i)
    utils.report_process("restart_elastic_index finished")


def elastic_builder(elastic_docs: list):
    utils.report_process("elastic_builder started!")
    es = utils.elastic_connect()
    mapping = {
        "mappings": {
            "properties": {
                "pin": {
                    "properties": {
                        "location": {
                            "type": "geo_point"
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index=constants.ELASTIC_INDEX, body=mapping)
    for doc in elastic_docs:
        es.index(index=constants.ELASTIC_INDEX, body=doc)
    utils.report_process("elastic_builder finished!")


def main():
    labels_file_number = None
    first_file = sys.argv[1] if len(sys.argv) > 1 else 0  # the first number file can be received as a parameter so the process can be started from the middle

    try:
        utils.init_report_file()
        utils.report_process("============== Start elastic builder ==============")
        if first_file == 0:
            split_file.split_file()  # split the labels file

        _, _, label_files = next(os.walk(constants.SPLIT_LABELS_DIRECTORY_PATH))  # gets the number of the files the labels were split
        for file_number in range(first_file, len(label_files)):  # parse data and save it in separate files
            labels_file_number = file_number
            parse_labels.parse_labels(file_number)

        labels_file_number = None
        labels_dict = []
        for file_number in range(len(label_files)):  # unify all files into one dict
            with open(f'{constants.DICT_LABELS_FILE_PATH}{file_number}{constants.DICT_LABELS_FILE_EXTENSION}', "rb") as labels_dict_file:
                labels_dict.extend(pickle.load(labels_dict_file))

        restart_elastic_index()
        elastic_builder(labels_dict)

        utils.report_process("============== Finish Successfully!!!! ==============")

    except Exception as e:
        utils.report_process(f'Finish With Exception: {e}')
        if labels_file_number is not None:
            utils.report_process(f'Finished in labels file: {labels_file_number}')


if __name__ == "__main__":
    main()
