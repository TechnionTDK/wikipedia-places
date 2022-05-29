import json
import re
from datetime import datetime
from elasticsearch import Elasticsearch
from typing import Tuple, Any
import constants


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


def report_process(report: Any):
    with open(constants.REPORT_FILE_FILE_PATH, "a+") as report_file:
        report = f'{datetime.today().strftime("%d/%m/%Y %H:%M:%S")}: {str(report)}\n'
        report_file.write(report)
        print(report)


def elastic_connect() -> Elasticsearch:
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def full_address_to_displayed_address(address: str) -> str:
    address_tokens = address.replace('״', '"').split(",")
    return ",".join(address_tokens[0:min(len(address_tokens), constants.DEFAULT_WORDS_IN_PLACE_NAME)])


def filter_suggestions(pattern: str) -> str:
    pattern = re.sub(r'[0-9]', "", pattern)
    pattern = pattern.replace("רחוב", "").replace("שדרה", "").replace("רחוב", "").replace("מספר", "").replace("רחוב", "").replace('״', '"').replace(" ", "+").replace("++", "+")

    if len(pattern) and pattern[0] == "+":
        pattern = pattern[1:]

    if len(pattern) and pattern[-1] == "+":
        pattern = pattern[0: -1]

    return pattern
