import json
from elastic_builder import constants
import utils


def split_file():
    utils.report_process("split_file begins")
    with open(constants.ALL_LABELS_FILE_PATH, "r", encoding='utf-8') as labels_file:
        labels, count, file_number, file = [], 0, 0, None
        for line in json.load(labels_file):
            if count % constants.LABELS_FILE_AMOUNT == 0:
                if file:
                    json.dump(labels, file, ensure_ascii=False)
                    labels = []
                    file.close()
                file = open(f'{constants.SPLIT_LABELS_DIRECTORY_PATH}{constants.SPLIT_LABELS_FILE_PATH}{str(file_number)}{constants.LABELS_FILE_EXTENSION}', 'w')
                file_number += 1
            labels.append(line)
            count += 1
    utils.report_process("split_file ends")
