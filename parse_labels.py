import re
import requests
import pickle
from elastic_builder import constants
import utils

S = requests.Session()


class DataLoad:
    def __init__(self, filepath: str):
        self.all_labels, self.labels_to_urls = utils.labels_from_json(labels_path=filepath)


def coordinates_on_earth(full_coordinates: dict) -> bool:
    return abs(full_coordinates['lat']) <= 90 and abs(full_coordinates['lon']) <= 180


def filter_abstract(abstract: str) -> str:
    abstract = re.sub(r'[0-9]+[p][x]', "", abstract)
    abstract = re.sub(r'(<[a-z]*>)', "", abstract)
    abstract = abstract.replace("_", " ").replace("{", "").replace("}", "").replace("=", " ").replace("|", "").replace("==", "").replace("\n\n", "").replace("  ", " ")

    abstract = abstract.split('ראו גם')[0]
    abstract = abstract.split('לקריאה נוספת')[0]
    abstract = abstract.split('קישורים חיצוניים')[0]
    abstract = abstract.split('הערות שוליים')[0]

    if len(abstract) and abstract[0] == " ":
        abstract = abstract[1:]

    if len(abstract) and abstract[-1] == " ":
        abstract = abstract[0: -1]

    abstract_sentences = abstract.split(".")
    return " ".join(abstract_sentences[0:min(constants.DEFAULT_MIN_ABSTRACT_SENTENCES + 1, len(abstract_sentences))])


def get_image_url(images: list) -> str:
    for image in images:
        if 'title' in image and constants.ALLOWED_IMAGE_SUFFIX in image['title']:
            params = {
                "action": "query",
                "titles": image['title'].replace("קובץ", 'File').replace(" ", "_"),
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json"
            }
            image_info = S.get(url=constants.WIKIPEDIA_API_URL, params=params).json()['query']['pages']
            if '-1' in image_info and 'imageinfo' in image_info['-1'] and len(image_info['-1']['imageinfo']) and 'url' in \
                    image_info['-1']['imageinfo'][0]:
                return image_info['-1']['imageinfo'][0]['url']
    return ""


def add_data_to_doc(data: DataLoad, file_number: int):
    with open(f'{constants.DICT_LABELS_FILE_PATH}{file_number}{constants.DICT_LABELS_FILE_EXTENSION}', "wb") as labels_dict_file:
        params = {
            "action": "query",
            "format": "json",
            "titles": "",
            "prop": "coordinates|images|extracts",
            "explaintext": 1
        }
        dictionary_data = []

        for label in data.all_labels:
            params["titles"] = label
            for label_key, label_value in S.get(url=constants.WIKIPEDIA_API_URL, params=params).json()['query']['pages'].items():
                utils.report_process(label)
                if 'coordinates' in label_value and coordinates_on_earth(label_value['coordinates'][0]):
                    pin = {"location": {
                        "lat": label_value['coordinates'][0]['lat'],
                        "lon": label_value['coordinates'][0]['lon']
                    }}

                    doc = {
                        "label": label,
                        "pin": pin,
                        "url": data.labels_to_urls[label],
                        "abstract": filter_abstract(label_value['extract']),
                        "imageUrl": get_image_url(label_value['images']) if 'images' in label_value else ''
                    }
                    dictionary_data.append(doc)
                    utils.report_process(doc)

        pickle.dump(dictionary_data, labels_dict_file)


def parse_labels(file_number: int):
    filepath = f'{constants.SPLIT_LABELS_DIRECTORY_PATH}{constants.SPLIT_LABELS_FILE_PATH}{str(file_number)}{constants.LABELS_FILE_EXTENSION}'
    utils.report_process(f'{filepath} begins')
    add_data_to_doc(DataLoad(filepath), file_number)
    utils.report_process(f'{filepath} ends')
