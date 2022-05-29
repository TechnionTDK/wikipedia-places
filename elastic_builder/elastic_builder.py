import os
import requests
import sys
import pickle
from general import constants, utils
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


def elastic_builder(elastic_docs: dict):
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
        utils.report_process("start indexing label " + doc["label"] + "...")
        es.ELASTIC_INDEX(index=constants.ELASTIC_INDEX, body=doc)
        utils.report_process("finish indexing label " + doc["label"] + "...")
    utils.report_process("elastic_builder finished!")


def main():
    labels_file_number = ""
    try:
        utils.init_report_file()
        utils.report_process("============== Start elastic builder ==============")
        split_file.split_file()

        first_file = sys.argv[1] if len(sys.argv) > 1 else 0
        _, _, label_files = next(os.walk(constants.SPLIT_LABELS_DIRECTORY_PATH))
        for file_number in range(first_file, len(label_files)):
            labels_file_number = f'{constants.SPLIT_LABELS_DIRECTORY_PATH}{constants.SPLIT_LABELS_FILE_PATH}{str(file_number)}{constants.LABELS_FILE_EXTENSION}'
            parse_labels.parse_labels(labels_file_number)

        labels_file_number = None
        with open(constants.DICT_LABELS_FILE_PATH, "rb") as labels_dict_file:
            restart_elastic_index()
            elastic_builder(pickle.load(labels_dict_file))

        utils.report_process("============== Finish Successfully!!!! ==============")

    except Exception as e:
        utils.report_process(f'Finish With Exception: {e}')
        if labels_file_number is not None:
            utils.report_process(f'Finished in labels file: {labels_file_number}')


if __name__ == "__main__":
    main()
