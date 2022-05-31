import os
import requests
import sys
import pickle
import argparse
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


def parse_arguments():
    parser = argparse.ArgumentParser(description='Script for parsing the places data and indexing the elastic search')
    parser.add_argument("-f", "--file", help="File number for starting the parsing of the data (ignoring the files split). if --index arg is set, this arg is not relevant", type=int, default=0)
    parser.add_argument("-i", "--index", help="if is set, partially process is running- only restart and index of elastic search.", action="store_true")
    return parser.parse_args()


def main():
    labels_file_number = None
    args = parse_arguments()

    try:
        utils.init_report_file()
        utils.report_process("============== Start elastic builder ==============")
        if not args.index and args.file == 0:
            split_file.split_file()  # split the labels file

        _, _, label_files = next(os.walk(constants.SPLIT_LABELS_DIRECTORY_PATH))  # gets the number of the files the labels were split

        if not args.index:
            for file_number in range(args.file, len(label_files)):  # parse data and save it in separate files
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
