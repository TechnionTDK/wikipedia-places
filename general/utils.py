import json
from datetime import datetime
from elasticsearch import Elasticsearch
from typing import Tuple
from general import constants


def labels_from_json(labels_path: str) -> Tuple[list, dict]:
    with open(labels_path, "r", encoding='utf-8') as labels_file:
        labels, labels_property, labels_and_urls = [], {}, json.load(labels_file)
        for label_dict in labels_and_urls:
            label = label_dict['rdfs:label']
            labels.append(label)
            labels_property[label] = label_dict['uri']
    return labels, labels_property


def init_report_file():
    with open(constants.REPORT_FILE_FILE_PATH, "w") as report_file:
        report_file.write("")


def report_process(report):
    with open(constants.REPORT_FILE_FILE_PATH, "a+") as report_file:
        report = f'{datetime.today().strftime("%d/%m/%Y %H:%M:%S")}: {str(report)}\n'
        report_file.write(report)
        print(report)


def elastic_connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])
